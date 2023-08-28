from utilities import equals
from utilities import run_tests
from utilities import set_up_authorization_error_request
from utilities import set_up_owner_headers
from utilities import set_up_user_headers
from utilities import set_up_order_test
from utilities import evaluate_status_test
from utilities import evaluate_order_test
from utilities import set_up_user_headers_with_blockchain
from data      import get_order_error0
from data      import get_order_error1
from data      import get_order_error2
from data      import get_order_error3
from data      import get_order_error4
from data      import get_order_error5
from data      import get_order_error6
from data      import get_order_error7
from data      import get_order0
from data      import get_order_status0
from data      import get_order1
from data      import get_order_status1

def run_level1_tests ( with_authentication, authentication_url, customer_url, with_blockchain, customer_keys_path, customer_passphrase, owner_private_key, provider_url ):

    tests = [
        # Tests 1 - 11
        # These tests evaluate all possible errors that can occur when processing order requests 
        ["post", customer_url + "/order", set_up_authorization_error_request ( with_authentication ),             { }, { },                  { }, 401, { "msg": "Missing Authorization Header"                          }, equals, 1],
        ["post", customer_url + "/order", set_up_owner_headers ( with_authentication, authentication_url ),       { }, { },                  { }, 401, { "msg": "Missing Authorization Header"                          }, equals, 1],
        ["post", customer_url + "/order", set_up_user_headers ( with_authentication, False, authentication_url ), { }, { },                  { }, 401, { "msg": "Missing Authorization Header"                          }, equals, 1],
        ["post", customer_url + "/order", set_up_user_headers ( with_authentication, True, authentication_url ),  { }, { },                  { }, 400, { "message": "Field requests is missing."                        }, equals, 1],
        ["post", customer_url + "/order", set_up_user_headers ( with_authentication, True, authentication_url ),  { }, get_order_error0 ( ), { }, 400, { "message": "Product id is missing for request number 0."       }, equals, 1],
        ["post", customer_url + "/order", set_up_user_headers ( with_authentication, True, authentication_url ),  { }, get_order_error1 ( ), { }, 400, { "message": "Product quantity is missing for request number 1." }, equals, 1],
        ["post", customer_url + "/order", set_up_user_headers ( with_authentication, True, authentication_url ),  { }, get_order_error2 ( ), { }, 400, { "message": "Invalid product id for request number 0."          }, equals, 1],
        ["post", customer_url + "/order", set_up_user_headers ( with_authentication, True, authentication_url ),  { }, get_order_error3 ( ), { }, 400, { "message": "Invalid product id for request number 0."          }, equals, 1],
        ["post", customer_url + "/order", set_up_user_headers ( with_authentication, True, authentication_url ),  { }, get_order_error4 ( ), { }, 400, { "message": "Invalid product quantity for request number 0."    }, equals, 1],
        ["post", customer_url + "/order", set_up_user_headers ( with_authentication, True, authentication_url ),  { }, get_order_error5 ( ), { }, 400, { "message": "Invalid product quantity for request number 0."    }, equals, 1],
        ["post", customer_url + "/order", set_up_user_headers ( with_authentication, True, authentication_url ),  { }, get_order_error6 ( ), { }, 400, { "message": "Invalid product for request number 0."             }, equals, 1],

        # Tests 12 - 14
        # These tests evaluate errors that can occur when processing order requests when blockchain is used 
        # These tests will be skipped if --with-blockchain is not spefied
        ["post", customer_url + "/order", set_up_user_headers_with_blockchain ( with_authentication, True, authentication_url, with_blockchain, None ),     { }, get_order_error7 ( ), { }, 400, { "message": "Field address is missing." }, equals, 1],
        ["post", customer_url + "/order", set_up_user_headers_with_blockchain ( with_authentication, True, authentication_url, with_blockchain, "" ),       { }, get_order_error7 ( ), { }, 400, { "message": "Field address is missing." }, equals, 1],
        ["post", customer_url + "/order", set_up_user_headers_with_blockchain ( with_authentication, True, authentication_url, with_blockchain, "asdasd" ), { }, get_order_error7 ( ), { }, 400, { "message": "Invalid address."          }, equals, 1],

        # Tests 15 - 17
        # These tests evaluate all possible errors that can occur when processing status requests
        # Since there are no parameters, only errors that can occur are the ones regarding authorization and authentication (no token in headers or wrong token in headers)
        ["get", customer_url + "/status", set_up_authorization_error_request ( with_authentication ),             { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", customer_url + "/status", set_up_owner_headers ( with_authentication, authentication_url ),       { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", customer_url + "/status", set_up_user_headers ( with_authentication, False, authentication_url ), { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],

        # Tests 18 - 19
        # These tests evaluate order and status request (one order is shown)
        ["post", customer_url + "/order", set_up_order_test ( with_authentication, authentication_url, customer_url, with_blockchain, customer_keys_path, customer_passphrase ), { }, get_order0 ( ), { }, 200, { }, evaluate_order_test ( with_blockchain, owner_private_key, provider_url ), 2],

        ["get", customer_url + "/status", set_up_user_headers ( with_authentication, True, authentication_url ), { }, { }, { }, 200, get_order_status0 ( ) , evaluate_status_test, 7],

        # Tests 20 - 21
        # These tests evaluate order and status request (two orders are shown)
        ["post", customer_url + "/order", set_up_order_test ( with_authentication, authentication_url, customer_url, with_blockchain, customer_keys_path, customer_passphrase ), { }, get_order1 ( ), { }, 200, { }, evaluate_order_test ( with_blockchain, owner_private_key, provider_url ), 2],

        ["get", customer_url + "/status", set_up_user_headers ( with_authentication, True, authentication_url ), { }, { }, { }, 200, get_order_status1 ( ), evaluate_status_test, 7],
    ]

    percentage = run_tests ( tests )

    return percentage
