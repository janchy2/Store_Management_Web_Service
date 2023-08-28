from flask import Flask, request, Response, jsonify, make_response
from models import User, database
from sqlalchemy import and_
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, verify_jwt_in_request
from configuration import Configuration
import re


application = Flask(__name__)
application.config.from_object(Configuration)
jwt = JWTManager(application)

regexEmail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


@application.route("/register_customer", methods=["POST"])
def registerCustomer():
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    #provera da li su sva polja uneta
    missing = ""
    if (len(forename) == 0):
        missing = "forename"
    elif (len(surname) == 0):
        missing = "surname"
    elif (len(email) == 0):
        missing = "email"
    elif (len(password) == 0):
        missing = "password"

    if (len(missing) != 0):
        response = jsonify(message=f"Field {missing} is missing.")
        return make_response(response, 400)

    # provera da li je mejl odgovarajuceg formata
    if (not re.search(regexEmail, email)):
        response = jsonify(message="Invalid email.")
        return make_response(response, 400)

    # provera da li je lozinka odgovarajuce duzine
    if (len(password) < 8):
        response = jsonify(message="Invalid password.")
        return make_response(response, 400)

    # provera da li postoji korisnik sa istom mejl adresom
    user = User.query.filter(User.email == email).first()
    if (user):
        response = jsonify(message="Email already exists.")
        return make_response(response, 400)

    #kreiranje novog kupca
    customer = User(email=email, forename=forename, surname=surname, password=password, role="customer")
    database.session.add(customer)
    database.session.commit()

    return Response(status=200)


@application.route("/register_courier", methods=["POST"])
def registerCourier():
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    #provera da li su sva polja uneta
    missing = ""
    if(len(forename) == 0):
        missing = "forename"
    elif(len(surname) == 0):
        missing = "surname"
    elif(len(email) == 0):
        missing = "email"
    elif(len(password) == 0):
        missing = "password"

    if (len(missing) != 0):
        response = jsonify(message=f"Field {missing} is missing.")
        return make_response(response, 400)

    #provera da li je mejl odgovarajuceg formata
    if (not re.search(regexEmail, email)):
        response = jsonify(message="Invalid email.")
        return make_response(response, 400)

    #provera da li je lozinka odgovarajuce duzine
    if(len(password) < 8):
        response = jsonify(message="Invalid password.")
        return make_response(response, 400)

    #provera da li postoji korisnik sa istom mejl adresom
    user = User.query.filter(User.email == email).first()
    if (user):
        response = jsonify(message="Email already exists.")
        return make_response(response, 400)

    #kreiranje novog kurira
    courier = User(email=email, forename=forename, surname=surname, password=password, role="courier")
    database.session.add(courier)
    database.session.commit()

    return Response(status=200)


@application.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    # provera da li su sva polja uneta
    missing = ""
    if (len(email) == 0):
        missing = "email"
    elif (len(password) == 0):
        missing = "password"
    if (len(missing) != 0):
        response = jsonify(message=f"Field {missing} is missing.")
        return make_response(response, 400)

    # provera da li je mejl odgovarajuceg formata
    if (not re.search(regexEmail, email)):
        response = jsonify(message="Invalid email.")
        return make_response(response, 400)

    # provera da li korisnik postoji
    user = User.query.filter(and_(User.email == email, User.password == password)).first()
    if(not user):
        response = jsonify(message="Invalid credentials.")
        return make_response(response, 400)

    # dodela tokena
    additionalClaims = {
        "forename": user.forename,
        "surname": user.surname,
        "password": user.password,
        "role": user.role
    }
    accessToken = create_access_token(identity=user.email, additional_claims=additionalClaims)

    response = jsonify(accessToken=accessToken)
    return make_response(response, 200)


@application.route("/delete", methods=["POST"])
def delete():
    # provera da li postoji zaglavlje sa tokenom
    try:
        verify_jwt_in_request()
    except Exception:
        response = jsonify(msg="Missing Authorization Header")
        return make_response(response, 401)

    # provera da li postoji korisnik sa datim mejlom
    identity = get_jwt_identity()
    user = User.query.filter(User.email == identity).first()
    if(user):
        database.session.delete(user)
        database.session.commit()

        return Response(status=200)

    response = jsonify(message="Unknown user.")
    return make_response(response, 400)


if(__name__ == "__main__"):
    database.init_app(application)
    application.run(debug=True, host='0.0.0.0', port=5001)
