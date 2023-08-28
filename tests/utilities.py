import re
import datetime
import json
import secrets

from dateutil import parser
from requests import request
from copy     import deepcopy
from data     import get_user
from data     import get_is_user_registered
from data     import set_is_user_registered

from web3 import Account
from web3 import Web3
from web3 import HTTPProvider

def recursive_compare ( expected, received, level = 'root', preprocess_list = None, preprocess_scalar = None ):
    message = ""
    same    = True

    if ( isinstance ( expected, dict ) and isinstance ( received, dict ) ):
        if ( sorted ( expected.keys ( ) ) != sorted ( received.keys ( ) ) ):
            expected_key_set = set ( expected.keys ( ) )
            received_key_set = set ( received.keys ( ) )

            message += "{:<20} +{} -{}\n".format ( level, expected_key_set - received_key_set, received_key_set - expected_key_set )
            same     = False

            common_keys = expected_key_set & received_key_set
        else:
            common_keys = set ( expected.keys ( ) )

        for key in common_keys:
            result = recursive_compare (
                expected[key],
                received[key],
                "{}.{}".format ( level, key ),
                preprocess_list,
                preprocess_scalar
            )

            message += result[0]
            same    &= result[1]

    elif ( isinstance ( expected, list ) and isinstance ( received, list ) ):
        if ( len ( expected ) != len ( received ) ):
            message += "{:<20} expected_length={} received_length={}\n".format ( level, len ( expected ), len ( received ) )
            same     = False
        else:
            if preprocess_list:
                ( expected, received ) = preprocess_list ( expected, received, level )

            for i in range ( len ( expected ) ):
                result = recursive_compare (
                    expected[i],
                    received[i],
                    '{}[{}]'.format ( level, i ),
                    preprocess_list,
                    preprocess_scalar
                )

                message += result[0]
                same &= result[1]
    else:
        if ( preprocess_scalar ):
            ( expected, received ) = preprocess_scalar ( expected, received, level )

        if ( expected != received ):
            message += "{:<20} {} != {}\n".format ( level, expected, received )
            same = False

    return ( message, same )

def copy_dictionary ( destination, source ):
    for key in source:
        destination [key] = deepcopy ( source [key] )

def are_equal ( list0, list1 ):
    difference = [item for item in ( list0 + list1 ) if ( ( item not in list0 ) or ( item not in list1 ) )]

    return len ( difference ) == 0

def set_up_pass_function ( url, headers, data, files ):
    return ( url, None, False )

def set_up_authorization_error_request ( with_authentication ):
    def implementation ( url, headers, data, files ):
        if ( not with_authentication ):
            return ( url, None, True )

        return ( url, None, False )

    return implementation

def owner_login ( authentication_url, headers ):
    response = request (
            method  = "post",
            url     = authentication_url + "/login",
            headers = { },
            json    = {
                    "email":    "onlymoney@gmail.com",
                    "password": "evenmoremoney"
            }
    )

    headers ["Authorization"] = "Bearer " + response.json ( ) ["accessToken"]

def set_up_owner_headers ( with_authentication, authentication_url ):
    def implementation ( url, headers, data, files ):
        if ( with_authentication ):
            owner_login ( authentication_url, headers )

        return ( url, None, False )

    return implementation

def user_login ( is_customer, authentication_url, headers ):
    if ( not get_is_user_registered ( is_customer ) ):
        url_suffix = "/register_customer" if ( is_customer ) else "/register_courier"
        response = request (
                method  = "post",
                url     = authentication_url + url_suffix,
                headers = { },
                json    = get_user ( is_customer )
        )
        set_is_user_registered ( is_customer, True )

    response = request (
            method  = "post",
            url     = authentication_url + "/login",
            headers = { },
            json    = {
                    "email":    get_user ( is_customer ) ["email"],
                    "password": get_user ( is_customer ) ["password"]
            }
    )

    headers ["Authorization"] = "Bearer " + response.json ( ) ["accessToken"]

def set_up_user_headers ( with_authentication, is_customer, authentication_url ):
    def implementation ( url, headers, data, files ):
        if ( with_authentication ):
            user_login ( is_customer, authentication_url, headers )

        return ( url, "", False )

    return implementation

def set_up_user_headers_with_blockchain ( with_authentication, is_customer, authentication_url, with_blockchain, address ):
    def implementation ( url, headers, data, files ):
        if ( with_authentication ):
            user_login ( is_customer, authentication_url, headers )
        
        if ( address is not None ):
            data["address"] = address

        return ( url, "", not with_blockchain )

    return implementation

def set_up_delete_test ( with_authentication, is_customer, authentication_url, tokens ):
    def implementation ( url, headers, data, files ):
        if ( with_authentication ):
            user_login ( is_customer, authentication_url, headers )

            tokens.append ( headers["Authorization"] )

        return ( url, "", False )

    return implementation

def set_up_delete_error_test ( with_authentication, tokens, index ):
    def implementation ( url, headers, data, files ):
        if ( with_authentication ):
            headers["Authorization"] = tokens[index]

        return ( url, "", False )

    return implementation

def equals ( set_up_data, expected_response, received_response ):
    assert expected_response == received_response, f"Invalid response, expected {expected_response}, received {received_response}."

def find_first ( list, predicate ):
    for item in list:
        if ( predicate ( item ) ):
            return item
    return None

PATH = "temp.csv"

def create_file ( path, content ):
    with open ( path, "w" ) as file:
        file.write ( content )

def set_up_update_test ( with_authentication, authentication_url, lines ):
    def implementation ( url, headers, data, files ):
        if ( with_authentication ):
            owner_login ( authentication_url, headers )

        create_file ( PATH, lines )
        file          = open ( PATH, "r" )
        files["file"] = file

        return ( url, None, False )

    return implementation

def set_up_search_test ( with_authentication, authentication_url, parameters ):
    def implementation ( url, headers, data, files ):
        if ( with_authentication ):
            user_login ( True, authentication_url, headers )

        return ( url + "?" + parameters, "", False  )

    return implementation

def evaluate_search_test ( set_up_data, expected_response, received_response ):
    def preprocess_list ( expected, received, level ):
        result = re.match (
            pattern = r"root.products\[\d\].categories",
            string  = level,
        )

        is_products   = level == "root.products"
        is_categories = ( result != None ) or ( level == "root.categories" )

        if ( is_products ):
            expected_sorted = sorted (
                expected,
                key = lambda item: item["name"]
            )
            received_sorted = sorted (
                received,
                key = lambda item: item["name"]
            )

            return ( list ( expected_sorted ), list ( received_sorted ) )
        elif ( is_categories ):
            expected_sorted = sorted ( expected )
            received_sorted = sorted ( received )

            return ( list ( expected_sorted ), list ( received_sorted ) )
        else:
            return ( expected, received )

    def preprocess_scalar ( expected, received, level ):
        result = re.match (
            pattern = r"root.products\[\d\].id",
            string  = level,
        )

        is_id = result != None

        if ( is_id ):
            if ( type ( received ) is int ):
                return (1, 1)
            else:
                return ( expected, received )
        else:
            return ( expected, received )


    ( message, same ) = recursive_compare ( expected_response, received_response, preprocess_list = preprocess_list, preprocess_scalar = preprocess_scalar )

    assert same, message

def get_empty_parameters_search_results ( with_authentication, authentication_url, customer_url ):
    headers = { }
    if ( with_authentication ):
        user_login ( True, authentication_url, headers )

    response = request (
        method  = "get",
        url     = customer_url + "/search",
        headers = headers,
        json    = { }
    )

    return response.json ( )

def load_address_from_keys_file ( keys_file_path, passphrase ):
    with open ( keys_file_path, "r" ) as file:
        private_key = Account.decrypt ( file.read ( ), passphrase )
        return Account.from_key ( private_key ).address
    

def set_up_order_test ( with_authentication, authentication_url, customer_url, with_blockchain, customer_keys_path, passphrase ):
    def implementation ( url, headers, data, files ):
        if ( with_authentication ):
            user_login ( True, authentication_url, headers )

        search_result = get_empty_parameters_search_results ( with_authentication, authentication_url, customer_url )

        products = search_result["products"]

        for index, request in enumerate ( data["requests"] ):
            product = find_first ( products, lambda item: item["name"] == request["id"] )

            data["requests"][index]["id"] = product["id"]

        if ( with_blockchain ):
            data["address"] = load_address_from_keys_file ( customer_keys_path, passphrase )

        return ( url, "", False )

    return implementation

def evaluate_status_test ( set_up_data, expected_response, received_response ):
    def preprocess_list ( expected, received, level ):
        products_result = re.match (
            pattern = r"^root.orders\[\d\].products$",
            string  = level,
        )

        categories_result = re.match (
            pattern = r"root.orders\[\d\].products\[\d\].categories",
            string  = level,
        )

        is_products   = products_result != None
        is_categories = categories_result != None

        if ( is_products ):
            expected_sorted = sorted (
                expected,
                key = lambda item: item["name"]
            )
            received_sorted = sorted (
                received,
                key = lambda item: item["name"]
            )

            return ( list ( expected_sorted ), list ( received_sorted ) )
        elif ( is_categories ):
            expected_sorted = sorted ( expected )
            received_sorted = sorted ( received )

            return ( list ( expected_sorted ), list ( received_sorted ) )
        else:
            return ( expected, received )

    def preprocess_scalar ( expected, received, level ):
        result = re.match (
            pattern = r"root.orders\[\d\].timestamp",
            string  = level,
        )

        is_timestamp = result != None

        result = re.match (
            pattern = r"root.orders\[\d\].price",
            string  = level,
        )

        is_price = result != None

        if ( is_timestamp ):
            try:
                receivedTime = parser.parse ( received )

                return ( 1, 1 )
            except ValueError as error:
                return ( 1, 2 )
        elif ( is_price ):
            if ( ( expected - 0.1 ) <= received <= ( expected + 0.1 ) ):
                return ( 1, 1 )
            else:
                return ( expected, received )
        else:
            return ( expected, received )


    ( message, same ) = recursive_compare ( expected_response, received_response, preprocess_list = preprocess_list, preprocess_scalar = preprocess_scalar )

    assert same, message

def evaluate_product_statistics_test ( set_up_data, expected_response, received_response ):
    def preprocess_list ( expected, received, level ):
        is_statistics = level == "root.statistics"

        if ( is_statistics ):
            expected_sorted = sorted (
                expected,
                key = lambda item: item["name"]
            )
            received_sorted = sorted (
                received,
                key = lambda item: item["name"]
            )

            return ( list ( expected_sorted ), list ( received_sorted ) )
        else:
            return ( expected, received )


    ( message, same ) = recursive_compare ( expected_response, received_response, preprocess_list = preprocess_list )

    assert same, message

def evaluate_category_statistics_test ( set_up_data, expected_response, received_response ):
    ( message, same ) = recursive_compare ( expected_response, received_response )

    assert same, message

def evaluate_transaction_from_latest_block ( address, name, provider_url ):
    web3 = Web3 ( HTTPProvider ( provider_url ) )
    block = web3.eth.get_block ( "latest", True )

    found = False
    for transaction in block.transactions:
        if ( transaction["from"] == address ):
            found = True
            break
    
    assert found, f"No transaction from {name} found in latest block."

def evaluate_order_test ( with_blockchain, owner_private_key, provider_url ):
    def implementation ( set_up_data, expected_response, received_response ):
        assert "id" in received_response, "Missing field id."
        assert type ( received_response["id"] ) is int, "ID must an integer greater than or equal to 0."
        assert int ( received_response["id"] ) >= 0, "ID must an integer greater than or equal to 0."

        if ( with_blockchain ):
            owner_address = Account.from_key ( owner_private_key ).address
            evaluate_transaction_from_latest_block ( owner_address, "owner", provider_url )
    
    return implementation

def evaluate_orders_to_pickup_test ( set_up_data, expected_response, received_response ):
    def preprocess_scalar ( expected, received, level ):
        result = re.match (
            pattern = r"root.orders\[\d\].id",
            string  = level,
        )

        is_id = result != None

        if ( is_id ):
            if ( type ( received ) is int ):
                return ( 1, 1 )
            else:
                return ( expected, received )
        else:
            return ( expected, received )


    ( message, same ) = recursive_compare ( expected_response, received_response, preprocess_list = None, preprocess_scalar = preprocess_scalar )

    assert same, message

def get_orders_to_deliver ( with_authentication, authentication_url, courier_url ):
    headers = { }
    if ( with_authentication ):
        user_login ( False, authentication_url, headers )

    response = request (
        method  = "get",
        url     = courier_url + "/orders_to_deliver",
        headers = headers,
        json    = { }
    )

    return response.json ( )

def set_up_delivered_error_test ( with_authentication, authentication_url, courier_url ):
    def implementation ( url, headers, data, files ):
        if ( with_authentication ):
            user_login ( True, authentication_url, headers )

        orders_to_deliver = get_orders_to_deliver ( with_authentication, authentication_url, courier_url )

        orders = orders_to_deliver["orders"]
        orders.sort ( key = lambda item: item["id"] )

        data["id"] = orders[0]["id"]

        return ( url, "", False  )

    return implementation

def set_up_pickup_order_test ( with_authentication, authentication_url, courier_url, order_ids, with_blockchain, courirer_private_key ):
    def implementation ( url, headers, data, files ):
        if ( with_authentication ):
            user_login ( False, authentication_url, headers )

        orders_to_deliver = get_orders_to_deliver ( with_authentication, authentication_url, courier_url )

        orders = orders_to_deliver["orders"]
        orders.sort ( key = lambda item: item["id"] )

        data["id"] = orders[0]["id"]

        order_ids.append ( data["id"] ) 

        if ( with_blockchain ):
            data["address"] = Account.from_key ( courirer_private_key ).address


        return ( url, "", False  )

    return implementation


def set_up_order_id ( with_authentication, authentication_url, is_customer, order_ids ):
    def implementation ( url, headers, data, files ):
        if ( with_authentication ):
            user_login ( is_customer, authentication_url, headers )

        data["id"] = order_ids[0]

        return ( url, "", False  )

    return implementation

def load_keys_file ( keys_file_path ):
    try:
        with open ( keys_file_path, "r" ) as file:
            return file.read ( )
    except Exception as error:
        return keys_file_path

def set_up_delivered_id ( with_authentication, authentication_url, is_customer, order_ids, with_blockchain, customer_keys_path, passhphrase  ):
    def implementation ( url, headers, data, files ):
        if ( with_authentication ):
            user_login ( is_customer, authentication_url, headers )

        data["id"] = order_ids.pop ( 0 )

        if ( with_blockchain ):
            if ( customer_keys_path is not None ):
                data["keys"] = load_keys_file ( customer_keys_path )

            if ( passhphrase is not None ):
                data["passphrase"] = passhphrase


        return ( url, "", False  )

    return implementation


def set_up_customer_headers_with_blockchain ( with_authentication, authentication_url, with_blockchain, customer_keys_path, passphrase ):
    def implementation ( url, headers, data, files ):
        if ( with_authentication ):
            user_login ( True, authentication_url, headers )
        
        if ( with_blockchain ):
            if ( customer_keys_path is not None ):
                data["keys"] = load_keys_file ( customer_keys_path )

            if ( passphrase is not None ):
                data["passphrase"] = passphrase

        return ( url, "", not with_blockchain )

    return implementation

def set_up_invalid_address ( with_authentication, authentication_url, courier_url, with_blockchain, order_ids, provider_url ):

    def implementation ( url, headers, data, files ):
        if ( with_authentication ):
            user_login ( True, authentication_url, headers )
        
        if ( with_blockchain ):
            passphrase  = "iep_project"
            private_key = "0x" + secrets.token_bytes ( 32 ).hex ( )
            address     = Account.from_key ( private_key ).address

            web3 = Web3 ( HTTPProvider ( provider_url ) )
            web3.eth.send_transaction ({
                "from": web3.eth.accounts[0],
                "to": address,
                "value": web3.to_wei ( 1, "ether" )
            })

            data["passphrase"] = passphrase
            data["keys"]       = str ( Account.encrypt ( private_key, passphrase ) )
        

        data["id"] = order_ids[0]

        return ( url, "", not with_blockchain )

    return implementation

def set_up_pay ( with_authentication, authentication_url, courier_url, with_blockchain, customer_keys_path, passphrase ):

    def implementation ( url, headers, data, files ):
        if ( with_authentication ):
            user_login ( True, authentication_url, headers )
        
        if ( with_blockchain ):
            data["keys"]       = load_keys_file ( customer_keys_path )
            data["passphrase"] = passphrase

        orders_to_deliver = get_orders_to_deliver ( with_authentication, authentication_url, courier_url )

        orders = orders_to_deliver["orders"]
        orders.sort ( key = lambda item: item["id"] )

        data["id"] = orders[0]["id"]

        return ( url, "", not with_blockchain )

    return implementation



def customer_equals ( with_blockchain, customer_keys_path, customer_passphrase, provider_url ):
    def implementation ( set_up_data, expected_response, received_response ):
        assert expected_response == received_response, f"Invalid response, expected {expected_response}, received {received_response}."

        if ( with_blockchain ):
            customer_address = Account.from_key ( Account.decrypt ( load_keys_file ( customer_keys_path ), customer_passphrase ) ).address
            evaluate_transaction_from_latest_block ( customer_address, "customer", provider_url )
    
    return implementation

def pick_up_order_equals ( with_blockchain, owner_private_key, provider_url ):
    def implementation ( set_up_data, expected_response, received_response ):
        assert expected_response == received_response, f"Invalid response, expected {expected_response}, received {received_response}."

        if ( with_blockchain ):
            owner_address = Account.from_key ( owner_private_key ).address
            evaluate_transaction_from_latest_block ( owner_address, "owner", provider_url )

    return implementation

def run_tests ( tests ):
    max   = 0
    total = 0

    for index, test in enumerate ( tests ):
        method                    = test [0]
        url                       = test [1]
        preparation_function      = test [2]
        headers                   = test [3]
        data                      = test [4]
        files                     = test [5]
        expected_status_code      = test [6]
        expected_response         = test [7]
        test_and_cleanup_function = test [8]
        score                     = test [9]


        try:
            ( url, set_up_data, skip_test ) = preparation_function ( url, headers, data, files )

            if ( not skip_test ):
                max   += score
                total += score

                response = request (
                        method  = method,
                        url     = url,
                        headers = headers,
                        json    = data,
                        files   = files
                )

                for key in files:
                    files[key].close ( )

                assert response.status_code == expected_status_code, f"Invalid status code, expected {expected_status_code}, received {response.status_code}"

                if ( expected_response is not None ):
                    received_response = response.json ( )
                else:
                    expected_response = { }
                    received_response = { }

                test_and_cleanup_function ( set_up_data, expected_response, received_response )
            else:
                print ( f"SKIPPED {index}" )

        except Exception as error:
            response_data = "DUMMY"
            try:
               response_data = response.json ( )
            except Exception as decode_error:
                pass 

            print ( f"Failed test number {index}\n\t method = {method}\n\t url = {url}\n\t headers = {headers}\n\t data = {data}\n\t files = {files}\n\t response = {response_data}\n\t error: {error}" )
            total -= score

    return total / max if ( max != 0 ) else 0
