from datetime  import datetime
from jwt       import decode
from requests  import request
from data      import get_user
from data      import set_is_user_registered
from utilities import equals
from utilities import set_up_pass_function
from utilities import set_up_owner_headers
from utilities import set_up_user_headers
from utilities import set_up_delete_test
from utilities import set_up_delete_error_test
from utilities import run_tests 

def user_register_equals ( is_customer ):
    def userRegisterEqualsImplementation ( set_up_data, expected_response, received_response ):
        equals ( set_up_data, expected_response, received_response )
        set_is_user_registered ( is_customer, True )

    return userRegisterEqualsImplementation

# This function evaluates the received token
def token_test ( 
    response,
    user, 
    token_field, 
    secret, 
    expected_type,
    expected_subject,
    expected_forename, 
    expected_surname, 
    roles_field, 
    expected_role, 
    expected_expires_delta 
):

    assert token_field in response, f"Login response error, {token_field} field missing for user {user}."

    token = decode ( response[token_field], key = secret, algorithms = ["HS256"], leeway = 60 )

    assert "nbf"       in token, f"{token_field} error for user {user}, field nbf is missing."
    assert "type"      in token, f"{token_field} error for user {user}, field type is missing."
    assert "exp"       in token, f"{token_field} error for user {user}, field exp is missing."
    assert "sub"       in token, f"{token_field} error for user {user}, field sub is missing."
    assert "forename"  in token, f"{token_field} error for user {user}, field forename is missing."
    assert "surname"   in token, f"{token_field} error for user {user}, field surname is missing."
    assert roles_field in token, f"{token_field} error for user {user}, field {roles_field} is missing."

    nbf      = token["nbf"]
    type     = token["type"]
    exp      = token["exp"]
    sub      = token["sub"]
    forename = token["forename"]
    surname  = token["surname"]
    roles    = token[roles_field]

    assert type     == expected_type                                 , f"{token_field} error for user {user}, field type has an incorrect value, expected {expected_type}, got {type}."
    assert sub      == expected_subject                              , f"{token_field} error for user {user}, field sub has an incorrect value, expected {expected_subject}, got {sub}."
    assert forename == expected_forename                             , f"{token_field} error for user {user}, field forename has an incorrect value, expected {expected_forename}, got {forename}."
    assert surname  == expected_surname                              , f"{token_field} error for user {user}, field surname has an incorrect value, expected {expected_surname}, got {surname}."
    assert ( roles   == expected_role ) or ( expected_role in roles ), f"{token_field} error for user {user}, field {roles_field} has an incorrect value, expected {expected_role}, got {roles}."

    expires_delta = datetime.fromtimestamp ( exp ) - datetime.fromtimestamp ( nbf )

    assert expires_delta.total_seconds ( ) == expected_expires_delta, f"{token_field} error for user {user}, expiration has an incorrect value, expected {expected_expires_delta}, got {expires_delta.total_seconds ( )}."


# Following functions are wrappers used to evaluate tokens for different users
def owner_token_test ( 
    response, 
    token_field, 
    secret, 
    expected_type, 
    roles_field, 
    expected_role, 
    expected_expires_delta 
):
    token_test (
        response               = response,
        user                   = "owner",
        token_field            = token_field,
        secret                 = secret,
        expected_type          = expected_type,
        expected_subject       = "onlymoney@gmail.com",
        expected_forename      = "Scrooge",
        expected_surname       = "McDuck",
        roles_field            = roles_field,
        expected_role          = expected_role,
        expected_expires_delta = expected_expires_delta
    )

def owner_access_token_test_wrapper ( response, secret, roles_field, expected_role ):
    owner_token_test (
        response               = response,
        token_field            = "accessToken",
        secret                 = secret,
        expected_type          = "access",
        roles_field            = roles_field,
        expected_role          = expected_role,
        expected_expires_delta = 60 * 60
    )

def owner_access_token_test ( jwt_secret, roles_field, owner_role ):
    def implementation ( set_up_data, expected_response, received_response ):
        owner_access_token_test_wrapper (
            response     = received_response,
            secret       = jwt_secret,
            roles_field   = roles_field,
            expected_role = owner_role
        )

    return implementation

def user_token_test ( is_customer, response, token_field, secret, expected_type, roles_field, expected_role, expected_expires_delta ):
    token_test (
        response               = response,
        user                   = get_user ( is_customer )["forename"] + get_user ( is_customer )["surname"],
        token_field            = token_field,
        secret                 = secret,
        expected_type          = expected_type,
        expected_subject       = get_user ( is_customer )["email"],
        expected_forename      = get_user ( is_customer )["forename"],
        expected_surname       = get_user ( is_customer )["surname"],
        roles_field            = roles_field,
        expected_role          = expected_role,
        expected_expires_delta = expected_expires_delta
    )

def user_access_token_test_wrapper ( is_customer, response, secret, roles_field, expected_role ):
    user_token_test (
        is_customer            = is_customer,
        response               = response,
        token_field            = "accessToken",
        secret                 = secret,
        expected_type          = "access",
        roles_field            = roles_field,
        expected_role          = expected_role,
        expected_expires_delta = 60 * 60
    )

def user_access_token_test ( is_customer, jwt_secret, roles_field, userRole ):
    def user_access_token_testImplementation ( set_up_data, expected_response, received_response ):
        user_access_token_test_wrapper (
            is_customer   = is_customer,
            response      = received_response,
            secret        = jwt_secret,
            roles_field   = roles_field,
            expected_role = userRole
        )

    return user_access_token_testImplementation


def user_delete_equals ( is_customer ):
    def implementation ( set_up_data, expected_response, received_response ):
        equals ( set_up_data, expected_response, received_response )
        set_is_user_registered ( is_customer, False )

    return implementation


def run_authentication_tests ( authentication_url, jwt_secret, roles_field, customer_role, courier_role, owner_role ):
    tokens = [ ]

    tests = [
        # Tests 1 - 17
        # These tests evaluate all possible errors that can occure when processing register requests 
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, {                                                                                               }, { }, 400, { "message": "Field forename is missing."   }, equals, 1],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, { "forename": ""                                                                                }, { }, 400, { "message": "Field forename is missing."   }, equals, 1],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, { "forename": " "                                                                               }, { }, 400, { "message": "Field surname is missing."    }, equals, 1],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, { "forename": " ",    "surname": ""                                                             }, { }, 400, { "message": "Field surname is missing."    }, equals, 1],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, { "forename": " ",    "surname": " "                                                            }, { }, 400, { "message": "Field email is missing."      }, equals, 1],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, { "forename": " ",    "surname": " ",   "email": ""                                             }, { }, 400, { "message": "Field email is missing."      }, equals, 1],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, { "forename": " ",    "surname": " ",   "email": " "                                            }, { }, 400, { "message": "Field password is missing."   }, equals, 1],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, { "forename": " ",    "surname": " ",   "email": " ",                   "password": ""          }, { }, 400, { "message": "Field password is missing."   }, equals, 1],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": " ",                   "password": " "         }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": "john",                "password": " "         }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": "john@",               "password": " "         }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail",          "password": " "         }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail.",         "password": " "         }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail.a",        "password": " "         }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail.com",      "password": " "         }, { }, 400, { "message": "Invalid password."            }, equals, 1],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail.com",      "password": "aaaa"      }, { }, 400, { "message": "Invalid password."            }, equals, 1],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": "onlymoney@gmail.com", "password": "Aaaaaaaa1" }, { }, 400, { "message": "Email already exists."        }, equals, 1],

        # Tests 18 - 34 
        # These tests evaluate all possible errors that can occure when processing register requests 
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, {                                                                                               }, { }, 400, { "message": "Field forename is missing."   }, equals, 1],
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, { "forename": ""                                                                                }, { }, 400, { "message": "Field forename is missing."   }, equals, 1],
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, { "forename": " "                                                                               }, { }, 400, { "message": "Field surname is missing."    }, equals, 1],
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, { "forename": " ",    "surname": ""                                                             }, { }, 400, { "message": "Field surname is missing."    }, equals, 1],
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, { "forename": " ",    "surname": " "                                                            }, { }, 400, { "message": "Field email is missing."      }, equals, 1],
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, { "forename": " ",    "surname": " ",   "email": ""                                             }, { }, 400, { "message": "Field email is missing."      }, equals, 1],
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, { "forename": " ",    "surname": " ",   "email": " "                                            }, { }, 400, { "message": "Field password is missing."   }, equals, 1],
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, { "forename": " ",    "surname": " ",   "email": " ",                   "password": ""          }, { }, 400, { "message": "Field password is missing."   }, equals, 1],
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": " ",                   "password": " "         }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": "john",                "password": " "         }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": "john@",               "password": " "         }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail",          "password": " "         }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail.",         "password": " "         }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail.a",        "password": " "         }, { }, 400, { "message": "Invalid email."               }, equals, 1],
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail.com",      "password": " "         }, { }, 400, { "message": "Invalid password."            }, equals, 1],
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": "john@gmail.com",      "password": "aaaa"      }, { }, 400, { "message": "Invalid password."            }, equals, 1],
        ["post", authentication_url + "/register_courier", set_up_pass_function, { }, { "forename": "John", "surname": "Doe", "email": "onlymoney@gmail.com", "password": "Aaaaaaaa1" }, { }, 400, { "message": "Email already exists."        }, equals, 1],

        # Test 35 - 46
        # These tests evaluate all possible errors that can occure when processing login requests
        ["post", authentication_url + "/login", set_up_pass_function, { }, {                                                                                  }, { }, 400, { "message": "Field email is missing."    }, equals, 1],
        ["post", authentication_url + "/login", set_up_pass_function, { }, { "email": ""                                                                      }, { }, 400, { "message": "Field email is missing."    }, equals, 1],
        ["post", authentication_url + "/login", set_up_pass_function, { }, { "email": " "                                                                     }, { }, 400, { "message": "Field password is missing." }, equals, 1],
        ["post", authentication_url + "/login", set_up_pass_function, { }, { "email": " ",                         "password": ""                             }, { }, 400, { "message": "Field password is missing." }, equals, 1],
        ["post", authentication_url + "/login", set_up_pass_function, { }, { "email": "john",                      "password": " "                            }, { }, 400, { "message": "Invalid email."             }, equals, 1],
        ["post", authentication_url + "/login", set_up_pass_function, { }, { "email": "john@",                     "password": " "                            }, { }, 400, { "message": "Invalid email."             }, equals, 1],
        ["post", authentication_url + "/login", set_up_pass_function, { }, { "email": "john@gmail",                "password": " "                            }, { }, 400, { "message": "Invalid email."             }, equals, 1],
        ["post", authentication_url + "/login", set_up_pass_function, { }, { "email": "john@gmail.",               "password": " "                            }, { }, 400, { "message": "Invalid email."             }, equals, 1],
        ["post", authentication_url + "/login", set_up_pass_function, { }, { "email": "john@gmail.a",              "password": " "                            }, { }, 400, { "message": "Invalid email."             }, equals, 1],
        ["post", authentication_url + "/login", set_up_pass_function, { }, { "email": "john@gmail.com",            "password": "123"                          }, { }, 400, { "message": "Invalid credentials."       }, equals, 1],
        ["post", authentication_url + "/login", set_up_pass_function, { }, { "email": get_user ( True )["email"],  "password": get_user ( True )["password"]  }, { }, 400, { "message": "Invalid credentials."       }, equals, 1],
        ["post", authentication_url + "/login", set_up_pass_function, { }, { "email": get_user ( False )["email"], "password": get_user ( False )["password"] }, { }, 400, { "message": "Invalid credentials."       }, equals, 1],

        # Test 47
        # These tests evaluate all possible errors that can occure when processing delete requests 
        ["post", authentication_url + "/delete", set_up_pass_function, { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],

        # Tests 48 - 49
        # These tests evaluate responses in case of susccessfull registrations of a customer and courirer
        ["post", authentication_url + "/register_courier",  set_up_pass_function, { }, get_user ( False ), { }, 200, None, user_register_equals ( False ), 3],
        ["post", authentication_url + "/register_customer", set_up_pass_function, { }, get_user ( True ),  { }, 200, None, user_register_equals ( True ) , 3],

        # Test 50
        # These tests evaluate responses in case of susccessfull login of the owner
        ["post", authentication_url + "/login", set_up_pass_function, { }, { "email": "onlymoney@gmail.com", "password": "evenmoremoney" }, { }, 200, { }, owner_access_token_test ( jwt_secret, roles_field, owner_role ) , 3],

        # Tests 51 - 52
        # These tests evaluate responses in case of susccessfull login of a customer and courier
        ["post", authentication_url + "/login", set_up_pass_function, { }, { "email": get_user ( True ) ["email"], "password": get_user ( True ) ["password"] }, { }, 200, { }, user_access_token_test ( True, jwt_secret, roles_field, customer_role ) , 7],
        ["post", authentication_url + "/login", set_up_pass_function, { }, { "email": get_user ( False )["email"], "password": get_user ( False )["password"] }, { }, 200, { }, user_access_token_test ( False, jwt_secret, roles_field, courier_role ) , 7],

        # Test 53 - 54
        # These tests evaluate responses in case of susccessfull deletion of a customer and courier
        ["post", authentication_url + "/delete", set_up_delete_test ( True, False, authentication_url, tokens ), { }, { }, { }, 200, None, user_delete_equals ( False ), 2],
        ["post", authentication_url + "/delete", set_up_delete_test ( True, True, authentication_url, tokens ),  { }, { }, { }, 200, None, user_delete_equals ( True ),  2],

        # Test 55 - 56
        # These tests evaluate responses in case of login request using credentials of a deleted account
        ["post", authentication_url + "/login", set_up_pass_function, { }, { "email": get_user ( True ) ["email"], "password": get_user ( True ) ["password"] }, { }, 400, { "message": "Invalid credentials." }, equals, 3],
        ["post", authentication_url + "/login", set_up_pass_function, { }, { "email": get_user ( False )["email"], "password": get_user ( False )["password"] }, { }, 400, { "message": "Invalid credentials." }, equals, 3],

        # Test 57 - 58
        # These tests evaluate responses in case of repeated deletion of already deleted accounts
        ["post", authentication_url + "/delete", set_up_delete_error_test ( True, tokens, 0 ), { }, { }, { }, 400, { "message": "Unknown user." }, equals, 2],
        ["post", authentication_url + "/delete", set_up_delete_error_test ( True, tokens, 1 ), { }, { }, { }, 400, { "message": "Unknown user." }, equals, 2],
    ]

    percentage = run_tests ( tests )

    return percentage