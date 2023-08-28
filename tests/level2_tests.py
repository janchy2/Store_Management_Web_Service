from utilities import run_tests
from utilities import set_up_authorization_error_request
from utilities import equals 
from utilities import set_up_user_headers
from utilities import set_up_customer_headers_with_blockchain
from utilities import evaluate_orders_to_pickup_test
from utilities import set_up_pickup_order_test
from utilities import evaluate_status_test
from utilities import set_up_delivered_error_test
from utilities import set_up_order_id
from utilities import set_up_delivered_id
from utilities import set_up_user_headers_with_blockchain
from utilities import set_up_invalid_address
from utilities import set_up_pay
from utilities import customer_equals 
from utilities import pick_up_order_equals
from data      import get_pay_error0
from data      import get_pay_error1
from data      import get_pay_error2
from data      import get_pay_error3
from data      import get_pay_error4
from data      import get_orders_to_deliver_result0
from data      import get_order_to_pickup_error0
from data      import get_order_to_pickup_error1
from data      import get_order_to_pickup_error2
from data      import get_order_to_pickup_error3
from data      import get_order_to_pickup_error4
from data      import get_orders_to_deliver_result1
from data      import get_order_status2
from data      import get_delivered_error0
from data      import get_delivered_error1
from data      import get_delivered_error2
from data      import get_delivered_error3
from data      import get_delivered_error4
from data      import get_order_status3


def run_level2_tests ( with_authentication, authentication_url, customer_url, courier_url, with_blockchain, owner_private_key, customer_keys_path, customer_passphrase, courier_private_key, provider_url ):
    order_ids = [ ]

    error = [ ]

    class ListWrapper:
        def __init__ ( self, list ):
            self.list = list
        def pop ( self, index ):
            return self.list[index]

    orders_id_wrapper = ListWrapper ( order_ids )

    def with_blockchain_wrapper ( function, *arguments ):
        def implementation ( url, headers, data, files ):
            ( url, set_up_data, skip_test ) = function ( *arguments ) ( url, headers, data, files )
            if ( with_blockchain ):
                return ( url, set_up_data, skip_test )         
            else:
                return ( url, set_up_data, True )         
        
        return implementation

    tests = [
        # Tests 1 - 11
        # These tests evaluate all possible errors that can occur when processing pay requests 
        # These tests will be skipped if --with-blockchain is not spefied
        ["post", customer_url + "/pay", set_up_authorization_error_request ( with_authentication and with_blockchain ),                                                  { },                { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["post", customer_url + "/pay", with_blockchain_wrapper ( set_up_user_headers, with_authentication, False, authentication_url ),                                 { },                { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["post", customer_url + "/pay", set_up_customer_headers_with_blockchain ( with_authentication, authentication_url, with_blockchain, None, None ),                { }, get_pay_error0 ( ), { }, 400, { "message": "Missing order id."        }, equals, 1],
        ["post", customer_url + "/pay", set_up_customer_headers_with_blockchain ( with_authentication, authentication_url, with_blockchain, None, None ),                { }, get_pay_error1 ( ), { }, 400, { "message": "Invalid order id."        }, equals, 1],
        ["post", customer_url + "/pay", set_up_customer_headers_with_blockchain ( with_authentication, authentication_url, with_blockchain, None, None ),                { }, get_pay_error2 ( ), { }, 400, { "message": "Invalid order id."        }, equals, 1],
        ["post", customer_url + "/pay", set_up_customer_headers_with_blockchain ( with_authentication, authentication_url, with_blockchain, None, None ),                { }, get_pay_error3 ( ), { }, 400, { "message": "Invalid order id."        }, equals, 1],
        ["post", customer_url + "/pay", set_up_customer_headers_with_blockchain ( with_authentication, authentication_url, with_blockchain, None, None ),                { }, get_pay_error4 ( ), { }, 400, { "message": "Missing keys."            }, equals, 1],
        ["post", customer_url + "/pay", set_up_customer_headers_with_blockchain ( with_authentication, authentication_url, with_blockchain, "", None ),                  { }, get_pay_error4 ( ), { }, 400, { "message": "Missing keys."            }, equals, 1],
        ["post", customer_url + "/pay", set_up_customer_headers_with_blockchain ( with_authentication, authentication_url, with_blockchain, " ", None ),                 { }, get_pay_error4 ( ), { }, 400, { "message": "Missing passphrase."      }, equals, 1],
        ["post", customer_url + "/pay", set_up_customer_headers_with_blockchain ( with_authentication, authentication_url, with_blockchain, " ", "" ),                   { }, get_pay_error4 ( ), { }, 400, { "message": "Missing passphrase."      }, equals, 1],
        ["post", customer_url + "/pay", set_up_customer_headers_with_blockchain ( with_authentication, authentication_url, with_blockchain, customer_keys_path, "123" ), { }, get_pay_error4 ( ), { }, 400, { "message": "Invalid credentials."     }, equals, 1],

        # Tests 12 - 13
        # These tests evaluate all possible errors that can occur when retrieving undelivered orders
        ["get", courier_url + "/orders_to_deliver", set_up_authorization_error_request ( with_authentication ),            { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["get", courier_url + "/orders_to_deliver", set_up_user_headers ( with_authentication, True, authentication_url ), { }, { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],

        # Tests 14 - 19
        # These tests evaluate all possible errors that can occur when processing a courier request to pick up a undelivered order
        ["post", courier_url + "/pick_up_order", set_up_authorization_error_request ( with_authentication ),             { },                            { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["post", courier_url + "/pick_up_order", set_up_user_headers ( with_authentication, True, authentication_url ),  { },                            { }, { }, 401, { "msg": "Missing Authorization Header" }, equals, 1],
        ["post", courier_url + "/pick_up_order", set_up_user_headers ( with_authentication, False, authentication_url ), { }, get_order_to_pickup_error0 ( ), { }, 400, { "message": "Missing order id."        }, equals, 1],
        ["post", courier_url + "/pick_up_order", set_up_user_headers ( with_authentication, False, authentication_url ), { }, get_order_to_pickup_error1 ( ), { }, 400, { "message": "Invalid order id."        }, equals, 1],
        ["post", courier_url + "/pick_up_order", set_up_user_headers ( with_authentication, False, authentication_url ), { }, get_order_to_pickup_error2 ( ), { }, 400, { "message": "Invalid order id."        }, equals, 1],
        ["post", courier_url + "/pick_up_order", set_up_user_headers ( with_authentication, False, authentication_url ), { }, get_order_to_pickup_error3 ( ), { }, 400, { "message": "Invalid order id."        }, equals, 1],

        # Tests 20 - 23
        # These tests evaluate all possible errors that can occur when processing a courier request to pick up a undelivered order and blockchain is used
        # These tests will be skipped if --with-blockchain is not spefied
        ["post", courier_url + "/pick_up_order", set_up_user_headers_with_blockchain ( with_authentication, False, authentication_url, with_blockchain, None ),                                           { }, get_order_to_pickup_error4 ( ), { }, 400, { "message": "Missing address."         }, equals, 1],
        ["post", courier_url + "/pick_up_order", set_up_user_headers_with_blockchain ( with_authentication, False, authentication_url, with_blockchain, "" ),                                             { }, get_order_to_pickup_error4 ( ), { }, 400, { "message": "Missing address."         }, equals, 1],
        ["post", courier_url + "/pick_up_order", set_up_user_headers_with_blockchain ( with_authentication, False, authentication_url, with_blockchain, "aaaa" ),                                         { }, get_order_to_pickup_error4 ( ), { }, 400, { "message": "Invalid address."         }, equals, 1],
        ["post", courier_url + "/pick_up_order", with_blockchain_wrapper ( set_up_pickup_order_test, with_authentication, authentication_url, courier_url, error, with_blockchain, courier_private_key ), { },                            { }, { }, 400, { "message": "Transfer not complete."   }, equals, 1],
        
        # Tests 24 - 30
        # These tests evaluate all possible errors that can occur when processing delivered request         
        ["post", customer_url + "/delivered", set_up_authorization_error_request ( with_authentication ),                           { },                      { }, { }, 401, { "msg": "Missing Authorization Header"  }, equals, 1],
        ["post", customer_url + "/delivered", set_up_user_headers ( with_authentication, False, authentication_url ),               { },                      { }, { }, 401, { "msg": "Missing Authorization Header"  }, equals, 1],
        ["post", customer_url + "/delivered", set_up_user_headers ( with_authentication, True, authentication_url ),                { }, get_delivered_error0 ( ), { }, 400, { "message": "Missing order id."         }, equals, 1],
        ["post", customer_url + "/delivered", set_up_user_headers ( with_authentication, True, authentication_url ),                { }, get_delivered_error1 ( ), { }, 400, { "message": "Invalid order id."         }, equals, 1],
        ["post", customer_url + "/delivered", set_up_user_headers ( with_authentication, True, authentication_url ),                { }, get_delivered_error2 ( ), { }, 400, { "message": "Invalid order id."         }, equals, 1],
        ["post", customer_url + "/delivered", set_up_user_headers ( with_authentication, True, authentication_url ),                { }, get_delivered_error3 ( ), { }, 400, { "message": "Invalid order id."         }, equals, 1],
        ["post", customer_url + "/delivered", set_up_delivered_error_test ( with_authentication, authentication_url, courier_url ), { },                      { }, { }, 400, { "message": "Invalid order id."         }, equals, 1],

        # Test 31
        # This test retrieves all orders that need to be delivered in order to properly set up further tests        
        ["get", courier_url + "/orders_to_deliver", set_up_user_headers ( with_authentication, False, authentication_url ), { }, { }, { }, 200, get_orders_to_deliver_result0 ( ), evaluate_orders_to_pickup_test, 3],

        # Test 32
        # This test evaluates a pay request for the first order made in level 1 tests       
        ["post", customer_url + "/pay", set_up_pay ( with_authentication, authentication_url, courier_url, with_blockchain, customer_keys_path, customer_passphrase ), { }, { }, { }, 200, None, customer_equals ( with_blockchain, customer_keys_path, customer_passphrase, provider_url ), 3],

        # Test 33
        # This test evaluates a pay request error which occurs in case of a repeated payment       
        ["post", customer_url + "/pay", set_up_pay ( with_authentication, authentication_url, courier_url, with_blockchain, customer_keys_path, customer_passphrase ), { }, { }, { }, 400, { "message": "Transfer already complete." }, equals, 1],

        # Tests 34 - 36
        # These test evaluate a regular pick up request
        # The first of the two orders is picked up, then its status is checked
        ["post", courier_url + "/pick_up_order", set_up_pickup_order_test ( with_authentication, authentication_url, courier_url, order_ids, with_blockchain, courier_private_key ), { }, { }, { }, 200, None, pick_up_order_equals ( with_blockchain, owner_private_key, provider_url ), 4],

        ["get", courier_url + "/orders_to_deliver", set_up_user_headers ( with_authentication, False, authentication_url ), { }, { }, { }, 200, get_orders_to_deliver_result1 ( ), evaluate_orders_to_pickup_test, 2],

        ["get", customer_url + "/status", set_up_user_headers ( with_authentication, True, authentication_url ), { }, { }, { }, 200, get_order_status2 ( ), evaluate_status_test, 2],

        # Tests 37 - 42
        # These tests evaluate all possible errors that can occur when processing delivered request and when blockchain is used
        # These tests will be skipped if --with-blockchain is not spefied
        ["post", customer_url + "/delivered", set_up_customer_headers_with_blockchain ( with_authentication, authentication_url, with_blockchain, None, None ),                { }, get_delivered_error4 ( ), { }, 400, { "message": "Missing keys."             }, equals, 1],
        ["post", customer_url + "/delivered", set_up_customer_headers_with_blockchain ( with_authentication, authentication_url, with_blockchain, "", None ),                  { }, get_delivered_error4 ( ), { }, 400, { "message": "Missing keys."             }, equals, 1],
        ["post", customer_url + "/delivered", set_up_customer_headers_with_blockchain ( with_authentication, authentication_url, with_blockchain, " ", None ),                 { }, get_delivered_error4 ( ), { }, 400, { "message": "Missing passphrase."       }, equals, 1],
        ["post", customer_url + "/delivered", set_up_customer_headers_with_blockchain ( with_authentication, authentication_url, with_blockchain, " ", "" ),                   { }, get_delivered_error4 ( ), { }, 400, { "message": "Missing passphrase."       }, equals, 1],
        ["post", customer_url + "/delivered", set_up_customer_headers_with_blockchain ( with_authentication, authentication_url, with_blockchain, customer_keys_path, "123" ), { }, get_delivered_error4 ( ), { }, 400, { "message": "Invalid credentials."      }, equals, 1],
        ["post", customer_url + "/delivered", set_up_invalid_address ( with_authentication, authentication_url, courier_url, with_blockchain, order_ids, provider_url ),       { },                      { }, { }, 400, { "message": "Invalid customer account." }, equals, 1],

        # Test 43
        # This test evaluates a pick up order request for an order that has already been picked up      
        ["post", courier_url + "/pick_up_order", set_up_order_id ( with_authentication, authentication_url, False, order_ids ), { }, { }, { }, 400, { "message": "Invalid order id." }, equals, 1],
    
        # Tests 44 - 45
        # These tests evaluate a valid delivered request
        ["post", customer_url + "/delivered", set_up_delivered_id ( with_authentication, authentication_url, True, orders_id_wrapper, with_blockchain, customer_keys_path, customer_passphrase ), { },  { }, { }, 200, None, customer_equals ( with_blockchain, customer_keys_path, customer_passphrase, provider_url ), 3],

        ["get", customer_url + "/status", set_up_user_headers ( with_authentication, True, authentication_url ), { }, { }, { }, 200, get_order_status3 ( ), evaluate_status_test, 5],

        # Test 46
        # This test evaluates a pick up order request for an order that has already been delivered
        ["post", courier_url + "/pick_up_order", set_up_order_id ( with_authentication, authentication_url, False, order_ids ), { }, { }, { }, 400, { "message": "Invalid order id." }, equals, 1],
    ]

    percentage = run_tests ( tests )

    return percentage
