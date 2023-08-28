from flask import Flask, request, Response, jsonify, make_response
from datetime import datetime
from models import Product, database, Category, OrderProduct, Order, ProductCategory
from sqlalchemy import and_, or_
from flask_jwt_extended import JWTManager, get_jwt_identity
from configuration import Configuration
from decorators import roleCheck
from collections import OrderedDict
import re
from web3 import Web3
from web3 import HTTPProvider
from web3 import Account
import json

application = Flask(__name__)
application.config.from_object(Configuration)
jwt = JWTManager(application)

web3 = Web3(HTTPProvider('http://ganache-cli:8545'))

accounts = web3.eth.accounts

#generisanje adrese racuna vlasnika
ownerPrivateKey = bytes.fromhex("b64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60")
ownerAccount = Account.from_key(ownerPrivateKey)

#prebacivanje sredstava na racun vlasnika
result = web3.eth.send_transaction({
    "from": web3.eth.accounts[0],
    "to": ownerAccount.address,
    "value": web3.to_wei(2, "ether")
})

def read_file(path):
    with open(path, "r") as file:
        return file.read()


@application.route("/search", methods=["GET"])
@roleCheck(role="customer")
def search():
    name = request.args.get("name", "")
    category = request.args.get("category", "")

    rows = Category.query.join(ProductCategory).join(Product).with_entities(Category.name).filter(
        and_(Product.name.like(f"%{name}%"), Category.name.like(f"%{category}%"))).group_by(Category.id).all()
    categories = []
    for row in rows:
        categories.append(row[0])

    if category:
        rows = (
            Product.query.join(ProductCategory).join(Category).with_entities(
                Product.id, Product.name, Product.price).filter(and_(Product.name.like(f"%{name}%"),
                            Category.name.like(f"%{category}%"))).group_by(Product.id).all())
    #ako nije zadata kategorija, moraju da se ukljuce i proizvodi koji nemaju kategoriju
    else:
        rows = (
            Product.query.outerjoin(ProductCategory).outerjoin(Category, ProductCategory.categoryId == Category.id)
            .with_entities(Product.id, Product.name, Product.price)
            .filter(
                and_(Product.name.like(f"%{name}%"), or_(Category.name.like(f"%{category}%"), Category.name.is_(None))))
            .group_by(Product.id)
            .all())

    products = []
    for row in rows:
        product = Product.query.filter(Product.id == row[0]).first()
        cats = [cat.name for cat in product.categories]
        object = {
            "categories": cats,
            "id": row[0],
            "name": row[1],
            "price": row[2],
        }
        products.append(object)

    response = jsonify(categories=categories, products=products)
    return make_response(response, 200)


@application.route("/order", methods=["POST"])
@roleCheck(role="customer")
def order():
    requests = request.json.get("requests", "")
    #provera da li postoji polje requests
    if (len(requests) == 0):
        response = jsonify(message="Field requests is missing.")
        return make_response(response, 400)

    products = []
    currentRequest = 0
    price = 0
    for req in requests:
        #provera da li postoji polje id
        if (not "id" in req):
            response = jsonify(message=f"Product id is missing for request number {currentRequest}.")
            return make_response(response, 400)
        #provera da li postoji polje quantity
        if (not "quantity" in req):
            response = jsonify(message=f"Product quantity is missing for request number {currentRequest}.")
            return make_response(response, 400)
        #provera da li je id ispravan
        id = req["id"]
        if (not isinstance(id, int) or id <= 0):
            response = jsonify(message=f"Invalid product id for request number {currentRequest}.")
            return make_response(response, 400)
        id = int(id)

        #provera da li je kolicina ispravna
        quantity = req["quantity"]
        if (not isinstance(quantity, int) or quantity <= 0):
            response = jsonify(message=f"Invalid product quantity for request number {currentRequest}.")
            return make_response(response, 400)
        quantity = int(quantity)

        product = Product.query.filter(Product.id == id).first()

        #provera da li proizvod postoji u bazi
        if (not product):
            response = jsonify(message=f"Invalid product for request number {currentRequest}.")
            return make_response(response, 400)

        currentRequest += 1
        products.append((product, quantity))
        price += quantity * product.price

    address = request.json.get("address", "")
    # provera da li postoji polje address
    if (len(address) == 0):
        response = jsonify(message="Field address is missing.")
        return make_response(response, 400)

    #provera da li je adresa ispravna
    if(not re.match(r'^0x[a-fA-F0-9]{40}$', address)):
        response = jsonify(message="Invalid address.")
        return make_response(response, 400)


    bytecode = read_file("./Contract.bin")
    abi = read_file("./Contract.abi")

    contract = web3.eth.contract(bytecode=bytecode, abi=abi)

    # generisanje adrese racuna vlasnika
    ownerPrivateKey = bytes.fromhex("b64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60")
    ownerAccount = Account.from_key(ownerPrivateKey)

    nonce = web3.eth.get_transaction_count(ownerAccount.address)

    priceInWei = web3.to_wei(price, 'wei')
    # pravljenje pametnog ugovora
    transaction = contract.constructor(ownerAccount.address, address, priceInWei).build_transaction({
        "from": ownerAccount.address,
        "nonce": nonce,
        "gasPrice": 21000
    })

    signed_transaction = web3.eth.account.sign_transaction(transaction, ownerPrivateKey)
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

    #dodavanje nove narudzbine
    order = Order(price=price, status="CREATED", time=datetime.now(), customer=get_jwt_identity(),
        contractAddress=receipt.contractAddress)
    database.session.add(order)
    database.session.commit()

    #povezivanje proizvoda i narudzbine
    for product in products:
        orderProduct = OrderProduct(productId=product[0].id, orderId=order.id, quantity=[product[1]])
        database.session.add(orderProduct)
        database.session.commit()

    response = jsonify(id=order.id)
    return make_response(response, 200)


@application.route("/status", methods=["GET"])
@roleCheck(role="customer")
def status():
    customer = get_jwt_identity()
    outerlist = []
    orders = Order.query.filter(Order.customer == customer).with_entities(Order.id, Order.price,
        Order.status, Order.time).all()
    for order in orders:
        innerList = []
        products = Order.query.join(OrderProduct).join(Product).with_entities(
            Product.id, Product.name, Product.price, OrderProduct.quantity).filter(Order.id == order[0]).all()
        for product in products:
            prod = Product.query.filter(Product.id == product[0]).first()
            cats = [cat.name for cat in prod.categories]
            object = {
                "categories": cats,
                "name": product[1],
                "price": product[2],
                "quantity": product[3]
            }
            innerList.append(object)

        object = OrderedDict()
        object["products"] = innerList
        object["price"] = order[1]
        object["status"] = order[2]
        object["timestamp"] = order[3]
        outerlist.append(object)

    response = jsonify(orders=outerlist)
    return make_response(response, 200)


@application.route("/delivered", methods=["POST"])
@roleCheck(role="customer")
def delivered():
    id = request.json.get("id", "")
    #provera da li postoji polje id
    if(id == ""):
        response = jsonify(message="Missing order id.")
        return make_response(response, 400)

    #provera da li je id validan
    if(not isinstance(id, int) or id <= 0):
        response = jsonify(message="Invalid order id.")
        return make_response(response, 400)
    order = Order.query.filter(Order.id == id).first()
    if(not order):
        response = jsonify(message="Invalid order id.")
        return make_response(response, 400)
    if(order.status != "PENDING"):
        response = jsonify(message="Invalid order id.")
        return make_response(response, 400)

    keys = request.json.get("keys", "")
    # provera da li postoji polje keys
    if (keys == ""):
        response = jsonify(message="Missing keys.")
        return make_response(response, 400)

    passphrase = request.json.get("passphrase", "")
    # provera da li postoji polje passphrase
    if (passphrase == ""):
        response = jsonify(message="Missing passphrase.")
        return make_response(response, 400)

    contractAddress = order.contractAddress
    abi = read_file("./Contract.abi")

    contract = web3.eth.contract(address=contractAddress, abi=abi)

    # provera da li je adresa ispravna
    try:
        data = json.loads(keys)
        address = web3.to_checksum_address(data["address"])
    except Exception:
        response = jsonify(message="Invalid customer account.")
        return make_response(response, 400)

    # desifrovanje
    try:
        private_key = Account.decrypt(data, passphrase).hex()
    except Exception:
        response = jsonify(message="Invalid credentials.")
        return make_response(response, 400)


    #provera da li su sredstva prebacena
    paid = contract.functions.paid().call()
    if(not paid):
        response = jsonify(message="Transfer not complete.")
        return make_response(response, 400)

    #prebacivanje sredstava
    contract.functions.confirmDelivery().transact({
        "from": address,
    })

    order.status = "COMPLETE"
    database.session.commit()

    return Response(status=200)


@application.route("/pay", methods=["POST"])
@roleCheck(role="customer")
def pay():
    id = request.json.get("id", "")
    # provera da li postoji polje id
    if (id == ""):
        response = jsonify(message="Missing order id.")
        return make_response(response, 400)

    # provera da li je id validan
    if (not isinstance(id, int) or id <= 0):
        response = jsonify(message="Invalid order id.")
        return make_response(response, 400)
    order = Order.query.filter(Order.id == id).first()
    if (not order):
        response = jsonify(message="Invalid order id.")
        return make_response(response, 400)

    keys = request.json.get("keys", "")
    # provera da li postoji polje keys
    if (keys == ""):
        response = jsonify(message="Missing keys.")
        return make_response(response, 400)

    passphrase = request.json.get("passphrase", "")
    # provera da li postoji polje passphrase
    if (passphrase == ""):
        response = jsonify(message="Missing passphrase.")
        return make_response(response, 400)

    # desifrovanje
    try:
        data = json.loads(keys)
        private_key = Account.decrypt(data, passphrase).hex()
        address = web3.to_checksum_address(data["address"])
    except Exception:
        response = jsonify(message="Invalid credentials.")
        return make_response(response, 400)

    contractAddress = order.contractAddress
    abi = read_file("./Contract.abi")

    contract = web3.eth.contract(address=contractAddress, abi=abi)

    # provera da li je transfer vec izvrsen
    paid = contract.functions.paid().call()
    if (paid):
        response = jsonify(message="Transfer already complete.")
        return make_response(response, 400)

    contract.functions.payForOrder().transact({
        "from": address,
        "value": web3.to_wei(order.price, 'wei')
    })

    return Response(status=200)


if(__name__ == "__main__"):
    database.init_app(application)
    application.run(debug=True, port=5002, host="0.0.0.0")
