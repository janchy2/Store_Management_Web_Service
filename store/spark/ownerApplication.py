from flask import Flask, request, Response, jsonify, make_response
from models import Product, database, Category, ProductCategory
from flask_jwt_extended import JWTManager
from configuration import Configuration
from decorators import roleCheck
import csv
import io
import os
import subprocess
import re
import ast

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
    os.environ["SPARK_APPLICATION_PYTHON_LOCATION"] = "/app/productStatistics.py"
    os.environ["SPARK_SUBMIT_ARGS"] = \
        "--driver-class-path /app/mysql-connector-j-8.0.33.jar --jars /app/mysql-connector-j-8.0.33.jar"

    output = subprocess.check_output(["/template.sh"]).decode()
    pattern = r'RESULT:\n\[.*\]'
    result = re.findall(pattern, output, re.DOTALL | re.MULTILINE)[0]
    result = result[7:]
    result = ast.literal_eval(result)
    response = jsonify(statistics=result)
    return make_response(response, 200)


@application.route("/category_statistics", methods=["GET"])
@roleCheck(role="owner")
def categoryStatistics():
    os.environ["SPARK_APPLICATION_PYTHON_LOCATION"] = "/app/categoryStatistics.py"
    os.environ["SPARK_SUBMIT_ARGS"] = \
        "--driver-class-path /app/mysql-connector-j-8.0.33.jar --jars /app/mysql-connector-j-8.0.33.jar"

    output = subprocess.check_output(["/template.sh"]).decode()
    pattern = r'RESULT:\n\[.*\]'
    result = re.findall(pattern, output, re.DOTALL | re.MULTILINE)[0]
    result = result[7:]
    result = ast.literal_eval(result)
    response = jsonify(statistics=result)
    return make_response(response, 200)


if(__name__ == "__main__"):
    database.init_app(application)
    application.run(debug=True, port=5004, host="0.0.0.0")
