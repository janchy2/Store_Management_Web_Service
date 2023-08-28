from utilities import equals
from utilities import run_tests
from utilities import set_up_authorization_error_request
from utilities import set_up_owner_headers
from utilities import set_up_user_headers
from utilities import set_up_update_test
from utilities import set_up_search_test
from utilities import evaluate_search_test
from data      import get_csv_error0
from data      import get_csv_error1
from data      import get_csv_error2
from data      import get_data0
from data      import get_search_result0
from data      import get_csv_error3
from data      import get_search_parameters1
from data      import get_search_result1
from data      import get_search_parameters2
from data      import get_search_result2
from data      import get_search_parameters3
from data      import get_search_result3
from data      import get_search_parameters4
from data      import get_search_result4

def run_level0_tests ( with_authentication, authentication_url, owner_url, customer_url ):

    tests = [
        # Tests 1 - 7
        # These tests evaluate all possible errors that can occure when processing update requests
        ["post", owner_url + "/update", set_up_authorization_error_request ( with_authentication ),                         { }, { }, { }, 401, { "msg": "Missing Authorization Header"              }, equals, 1],
        ["post", owner_url + "/update", set_up_user_headers ( with_authentication, True, authentication_url ),              { }, { }, { }, 401, { "msg": "Missing Authorization Header"              }, equals, 1],
        ["post", owner_url + "/update", set_up_user_headers ( with_authentication, False, authentication_url ),             { }, { }, { }, 401, { "msg": "Missing Authorization Header"              }, equals, 1],
        ["post", owner_url + "/update", set_up_owner_headers ( with_authentication, authentication_url ),                   { }, { }, { }, 400, { "message": "Field file is missing."                }, equals, 1],
        ["post", owner_url + "/update", set_up_update_test ( with_authentication, authentication_url, get_csv_error0 ( ) ), { }, { }, { }, 400, { "message": "Incorrect number of values on line 2." }, equals, 1],
        ["post", owner_url + "/update", set_up_update_test ( with_authentication, authentication_url, get_csv_error1 ( ) ), { }, { }, { }, 400, { "message": "Incorrect price on line 1."            }, equals, 1],
        ["post", owner_url + "/update", set_up_update_test ( with_authentication, authentication_url, get_csv_error2 ( ) ), { }, { }, { }, 400, { "message": "Incorrect price on line 1."            }, equals, 1],

        # Tests 8 - 10
        # These tests evaluate all possible errors that can occure when processing search requests
        # Since parameters are optional, only errors that can occur are the ones regarding authorization and authentication (no token in headers or wrong token in headers)
        ["get", customer_url + "/search", set_up_authorization_error_request ( with_authentication ),             { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", customer_url + "/search", set_up_owner_headers ( with_authentication, authentication_url ),       { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", customer_url + "/search", set_up_user_headers ( with_authentication, False, authentication_url ), { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],

        # Tests 11 - 12
        # These tests evaluate update and empty search requests
        ["post", owner_url + "/update", set_up_update_test ( with_authentication, authentication_url, get_data0 ( ) ), { }, { }, { }, 200, None, equals, 1],

        ["get", customer_url + "/search", set_up_user_headers ( with_authentication, True, authentication_url ), { }, { }, { }, 200, get_search_result0 ( ) , evaluate_search_test, 7],

        # Tests 13 - 14
        # These tests evaluate an invalid update and empty search requests
        ["post", owner_url + "/update", set_up_update_test ( with_authentication, authentication_url, get_csv_error3 ( ) ), { }, { }, { }, 400, { "message": "Product Product0 already exists." }, equals, 1],

        ["get", customer_url + "/search", set_up_user_headers ( with_authentication, True, authentication_url ), { }, { }, { }, 200, get_search_result0 ( ), evaluate_search_test, 7],

        # Tests 15 - 18
        # These tests evaluate search requests with different search parameters
        ["get", customer_url + "/search", set_up_search_test ( with_authentication, authentication_url, get_search_parameters1 ( ) ), { }, { }, { }, 200, get_search_result1 ( ), evaluate_search_test, 3],
        ["get", customer_url + "/search", set_up_search_test ( with_authentication, authentication_url, get_search_parameters2 ( ) ), { }, { }, { }, 200, get_search_result2 ( ), evaluate_search_test, 3],
        ["get", customer_url + "/search", set_up_search_test ( with_authentication, authentication_url, get_search_parameters3 ( ) ), { }, { }, { }, 200, get_search_result3 ( ), evaluate_search_test, 3],
        ["get", customer_url + "/search", set_up_search_test ( with_authentication, authentication_url, get_search_parameters4 ( ) ), { }, { }, { }, 200, get_search_result4 ( ), evaluate_search_test, 3],
    ]

    percentage = run_tests ( tests )

    return percentage