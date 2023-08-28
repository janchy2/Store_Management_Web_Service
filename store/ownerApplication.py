from flask import Flask, request, Response, jsonify, make_response
from models import Product, database, Category, ProductCategory, Order, OrderProduct
from sqlalchemy import func, case, text, create_engine
from flask_jwt_extended import JWTManager
from configuration import Configuration
from decorators import roleCheck
import csv
import io

application = Flask(__name__)
application.config.from_object(Configuration)
jwt = JWTManager(application)


@application.route("/update", methods=["POST"])
@roleCheck(role="owner")
def update():
    # provera da li postoji polje file
    if(not "file" in request.files):
        response = jsonify(message="Field file is missing.")
        return make_response(response, 400)

    fileContent = request.files["file"].stream.read().decode("utf-8")
    stream = io.StringIO(fileContent)
    readerObject = csv.reader(stream)
    currentRow = 0
    products = []
    for row in readerObject:
        # provera da li linija sadrzi 3 vrednosti
        if(len(row) != 3):
            response = jsonify(message=f"Incorrect number of values on line {currentRow}.")
            return make_response(response, 400)
        # provera da li je cena ispravna
        try:
            price = float(row[2])
            if(price <= 0):
                response = jsonify(message=f"Incorrect price on line {currentRow}.")
                return make_response(response, 400)
        except Exception:
            response = jsonify(message=f"Incorrect price on line {currentRow}.")
            return make_response(response, 400)

        # provera da li vec postoji proizvod sa datim imenom
        name = Product.query.filter(Product.name == row[1]).first()
        if (name):
            response = jsonify(message="Product {} already exists.".format(row[1]))
            return make_response(response, 400)
        currentRow += 1
        product = row[1], price, row[0].split('|')
        products.append(product)

    for product in products:
        newProduct = Product(name=product[0], price=product[1])
        database.session.add(newProduct)
        database.session.commit()
        # dodavanje kategorije ako ne postoji i povezivanje
        for category in product[2]:
            newCategory = Category.query.filter(Category.name == category).first()
            if(not newCategory):
                newCategory = Category(name=category)
                database.session.add(newCategory)
                database.session.commit()
            connection = ProductCategory(productId=newProduct.id, categoryId=newCategory.id)
            database.session.add(connection)
            database.session.commit()

    return Response(status=200)


@application.route("/product_statistics", methods=["GET"])
@roleCheck(role="owner")
def productStatistics():
    list = []
    rows = Product.query.join(OrderProduct).join(Order).with_entities(
        Product.name, func.sum(case([(Order.status == "COMPLETE", OrderProduct.quantity)], else_=0)
            ), func.sum(case([(Order.status != "COMPLETE", OrderProduct.quantity)], else_=0))
                ).group_by(Product.id, Product.name).all()
    for row in rows:
        object = {
            "name": row[0],
            "sold": int(str(row[1])),
            "waiting": int(str(row[2]))
        }
        list.append(object)

    response = jsonify(statistics=list)
    return make_response(response, 200)


@application.route("/category_statistics", methods=["GET"])
@roleCheck(role="owner")
def categoryStatistics():
    engine = create_engine(Configuration.SQLALCHEMY_DATABASE_URI)

    query = """
        SELECT categories.name,
        SUM(CASE WHEN orders.status = 'COMPLETE' THEN orderproduct.quantity ELSE 0 END) AS completed
        FROM categories
        LEFT JOIN productcategory ON categories.id = productcategory.categoryId
        LEFT JOIN products ON products.id = productcategory.productId
        LEFT JOIN orderproduct ON products.id = orderproduct.productId
        LEFT JOIN orders ON orders.id = orderproduct.orderId
        GROUP BY categories.name
        ORDER BY completed DESC, categories.name ASC;
    """
    rows = engine.execute(text(query))

    list = []
    for row in rows:
        list.append(row[0])
    response = jsonify(statistics=list)
    return make_response(response, 200)


if(__name__ == "__main__"):
    database.init_app(application)
    application.run(debug=True, port=5004, host="0.0.0.0")
