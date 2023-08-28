from utilities import equals
from utilities import run_tests
from utilities import set_up_authorization_error_request
from utilities import set_up_owner_headers
from utilities import set_up_user_headers
from utilities import evaluate_product_statistics_test
from utilities import evaluate_category_statistics_test
from utilities import set_up_pickup_order_test
from utilities import set_up_delivered_id
from utilities import set_up_order_test
from utilities import evaluate_order_test
from utilities import evaluate_status_test
from utilities import set_up_pay
from utilities import customer_equals 
from utilities import pick_up_order_equals
from data      import get_product_statistics0
from data      import get_category_statistics0
from data      import get_product_statistics1
from data      import get_category_statistics1
from data      import get_order2
from data      import get_product_statistics2
from data      import get_category_statistics2
from data      import get_order_status4
from data      import get_product_statistics3
from data      import get_category_statistics3
from data      import get_order_status5
from data      import get_order3
from data      import get_product_statistics4
from data      import get_category_statistics4
from data      import get_order_status6
from data      import get_product_statistics5
from data      import get_category_statistics5
from data      import get_order_status6
from data      import get_order_status7

def run_level3_tests ( with_authentication, authentication_url, owner_url, customer_url, courier_url, with_blockchain, owner_private_key, customer_keys_path, customer_passphrase, courier_private_key, provider_url ):
    order_ids = [ ]
    tests = [
        # Tests 1 - 3
        # These tests evaluate errors that can occur when processing product statistics requests
        # Since there are no parameters, only errors that can occur are the ones regarding authorization and authentication (no token in headers or wrong token in headers)
        ["get", owner_url + "/product_statistics", set_up_authorization_error_request ( with_authentication ),             { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", owner_url + "/product_statistics", set_up_user_headers ( with_authentication, True, authentication_url ),  { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", owner_url + "/product_statistics", set_up_user_headers ( with_authentication, False, authentication_url ), { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],

        # Tests 4 - 6
        # These tests evaluate errors that can occur when processing category statistics requests
        # Since there are no parameters, only errors that can occur are the ones regarding authorization and authentication (no token in headers or wrong token in headers)
        ["get", owner_url + "/category_statistics", set_up_authorization_error_request ( with_authentication ),             { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", owner_url + "/category_statistics", set_up_user_headers ( with_authentication, True, authentication_url ),  { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", owner_url + "/category_statistics", set_up_user_headers ( with_authentication, False, authentication_url ), { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],

        # The remainder of the tests check product and category statistics before and after making and delivering orders
        # pay requests will be skipped if --with-blockchain is not specified

        # Tests 7 - 8
        # statistics 0
        ["get", owner_url + "/product_statistics" , set_up_owner_headers ( with_authentication, authentication_url ), { }, { }, { }, 200, get_product_statistics0 ( ) , evaluate_product_statistics_test , 5],
        ["get", owner_url + "/category_statistics", set_up_owner_headers ( with_authentication, authentication_url ), { }, { }, { }, 200, get_category_statistics0 ( ), evaluate_category_statistics_test, 5],

        # Tests 9 - 11
        # update statistics
        ["post", customer_url + "/pay",          set_up_pay ( with_authentication, authentication_url, courier_url, with_blockchain, customer_keys_path, customer_passphrase ),              { }, { }, { }, 200, None, customer_equals ( with_blockchain, customer_keys_path, customer_passphrase, provider_url ), 1],
        ["post", courier_url + "/pick_up_order", set_up_pickup_order_test ( with_authentication, authentication_url, courier_url, order_ids, with_blockchain, courier_private_key ),         { }, { }, { }, 200, None, pick_up_order_equals ( with_blockchain, owner_private_key, provider_url ),                  1],
        ["post", customer_url + "/delivered",    set_up_delivered_id ( with_authentication, authentication_url, True, order_ids, with_blockchain, customer_keys_path, customer_passphrase ), { }, { }, { }, 200, None, customer_equals ( with_blockchain, customer_keys_path, customer_passphrase, provider_url ), 1],

        # Tests 12 - 13
        # statistics 1
        ["get", owner_url + "/product_statistics" , set_up_owner_headers ( with_authentication, authentication_url ), { }, { }, { }, 200, get_product_statistics1 ( ) , evaluate_product_statistics_test , 5],
        ["get", owner_url + "/category_statistics", set_up_owner_headers ( with_authentication, authentication_url ), { }, { }, { }, 200, get_category_statistics1 ( ), evaluate_category_statistics_test, 5],

        # Test 14
        # update statistics
        ["post", customer_url + "/order", set_up_order_test ( with_authentication, authentication_url, customer_url, with_blockchain, customer_keys_path, customer_passphrase ), { }, get_order2 ( ), { }, 200, { }, evaluate_order_test ( with_blockchain, owner_private_key, provider_url ), 1],

        # Tests 15 - 16
        # statistics 2
        ["get", owner_url + "/product_statistics" , set_up_owner_headers ( with_authentication, authentication_url ), { }, { }, { }, 200, get_product_statistics2 ( ) , evaluate_product_statistics_test , 5],
        ["get", owner_url + "/category_statistics", set_up_owner_headers ( with_authentication, authentication_url ), { }, { }, { }, 200, get_category_statistics2 ( ), evaluate_category_statistics_test, 5],

        # Test 17
        # order status
        ["get", customer_url + "/status", set_up_user_headers ( with_authentication, True, authentication_url ), { }, { }, { }, 200, get_order_status4 ( ), evaluate_status_test, 2],

        # Tests 18 - 20
        # update statistics
        ["post", customer_url + "/pay",          set_up_pay ( with_authentication, authentication_url, courier_url, with_blockchain, customer_keys_path, customer_passphrase ),              { }, { }, { }, 200, None, customer_equals ( with_blockchain, customer_keys_path, customer_passphrase, provider_url ), 1],
        ["post", courier_url + "/pick_up_order", set_up_pickup_order_test ( with_authentication, authentication_url, courier_url, order_ids, with_blockchain, courier_private_key ),         { }, { }, { }, 200, None, pick_up_order_equals ( with_blockchain, owner_private_key, provider_url ),                  1],
        ["post", customer_url + "/delivered",    set_up_delivered_id ( with_authentication, authentication_url, True, order_ids, with_blockchain, customer_keys_path, customer_passphrase ), { }, { }, { }, 200, None, customer_equals ( with_blockchain, customer_keys_path, customer_passphrase, provider_url ), 1],

        # Tests 21 - 22
        # statistics 3
        ["get", owner_url + "/product_statistics" , set_up_owner_headers ( with_authentication, authentication_url ), { }, { }, { }, 200, get_product_statistics3 ( ) , evaluate_product_statistics_test , 5],
        ["get", owner_url + "/category_statistics", set_up_owner_headers ( with_authentication, authentication_url ), { }, { }, { }, 200, get_category_statistics3 ( ), evaluate_category_statistics_test, 5],

        # Test 23
        # order status
        ["get", customer_url + "/status", set_up_user_headers ( with_authentication, True, authentication_url ), { }, { }, { }, 200, get_order_status5 ( ), evaluate_status_test, 2],

        # Test 24
        # update statistics
        ["post", customer_url + "/order", set_up_order_test ( with_authentication, authentication_url, customer_url, with_blockchain, customer_keys_path, customer_passphrase ), { }, get_order3 ( ), { }, 200, { }, evaluate_order_test ( with_blockchain, owner_private_key, provider_url ), 1],

        # Tests 25 - 26
        # statistics 4
        ["get", owner_url + "/product_statistics" , set_up_owner_headers ( with_authentication, authentication_url ), { }, { }, { }, 200, get_product_statistics4 ( ) , evaluate_product_statistics_test , 5],
        ["get", owner_url + "/category_statistics", set_up_owner_headers ( with_authentication, authentication_url ), { }, { }, { }, 200, get_category_statistics4 ( ), evaluate_category_statistics_test, 5],

        # Test 27
        # order status
        ["get", customer_url + "/status", set_up_user_headers ( with_authentication, True, authentication_url ), { }, { }, { }, 200, get_order_status6 ( ), evaluate_status_test, 2],

        # Tests 28 - 30
        # update statistics
        ["post", customer_url + "/pay",          set_up_pay ( with_authentication, authentication_url, courier_url, with_blockchain, customer_keys_path, customer_passphrase ),              { }, { }, { }, 200, None, customer_equals ( with_blockchain, customer_keys_path, customer_passphrase, provider_url ), 1],
        ["post", courier_url + "/pick_up_order", set_up_pickup_order_test ( with_authentication, authentication_url, courier_url, order_ids, with_blockchain, courier_private_key ),         { }, { }, { }, 200, None, pick_up_order_equals ( with_blockchain, owner_private_key, provider_url ),                  1],
        ["post", customer_url + "/delivered",    set_up_delivered_id ( with_authentication, authentication_url, True, order_ids, with_blockchain, customer_keys_path, customer_passphrase ), { }, { }, { }, 200, None, customer_equals ( with_blockchain, customer_keys_path, customer_passphrase, provider_url ), 1],

        # Tests 31 - 32
        # statistics 5
        ["get", owner_url + "/product_statistics" , set_up_owner_headers ( with_authentication, authentication_url ), { }, { }, { }, 200, get_product_statistics5 ( ) , evaluate_product_statistics_test, 5],
        ["get", owner_url + "/category_statistics", set_up_owner_headers ( with_authentication, authentication_url ), { }, { }, { }, 200, get_category_statistics5( ), evaluate_category_statistics_test, 5],

        # Test 33
        # order status
        ["get", customer_url + "/status", set_up_user_headers ( with_authentication, True, authentication_url ), { }, { }, { }, 200, get_order_status7 ( ), evaluate_status_test, 2],
    ]

    percentage = run_tests ( tests )

    return percentage
