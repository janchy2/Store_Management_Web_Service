from flask import Flask, request, Response, jsonify, make_response
from models import database, Order
from flask_jwt_extended import JWTManager
from configuration import Configuration
from decorators import roleCheck
import re
from web3 import Web3
from web3 import HTTPProvider
from web3 import Account

application = Flask(__name__)
application.config.from_object(Configuration)
jwt = JWTManager(application)

web3 = Web3(HTTPProvider('http://ganache-cli:8545'))

def read_file (path):
    with open(path, "r") as file:
        return file.read()


@application.route("/orders_to_deliver", methods=["GET"])
@roleCheck(role="courier")
def ordersToDeliver():
    orders = Order.query.filter(Order.status == "CREATED").with_entities(Order.id, Order.customer).all()
    list = []
    for order in orders:
        object = {
            "id": order[0],
            "email": order[1]
        }
        list.append(object)

    response = jsonify(orders=list)
    return make_response(response, 200)


@application.route("/pick_up_order", methods=["POST"])
@roleCheck(role="courier")
def pickUpOrder():
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
    if (order.status != "CREATED"):
        response = jsonify(message="Invalid order id.")
        return make_response(response, 400)

    address = request.json.get("address", "")
    # provera da li postoji polje address
    if (len(address) == 0):
        response = jsonify(message="Missing address.")
        return make_response(response, 400)

    # provera da li je adresa ispravna
    if (not re.match(r'^0x[a-fA-F0-9]{40}$', address)):
        response = jsonify(message="Invalid address.")
        return make_response(response, 400)


    contractAddress = order.contractAddress
    abi = read_file("./Contract.abi")

    contract = web3.eth.contract(address=contractAddress, abi=abi)

    # generisanje adrese racuna vlasnika
    ownerPrivateKey = bytes.fromhex("b64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60")
    ownerAccount = Account.from_key(ownerPrivateKey)

    # provera da li su sredstva prebacena
    paid = contract.functions.paid().call()
    if (not paid):
        response = jsonify(message="Transfer not complete.")
        return make_response(response, 400)

    #povezivanje kurira za ugovor
    contract.functions.addCourier(address).transact({
        "from": ownerAccount.address,
    })

    order.status = "PENDING"
    database.session.commit()
    return Response(status=200)



if(__name__ == "__main__"):
    database.init_app(application)
    application.run(debug=True, port=5003, host="0.0.0.0")
