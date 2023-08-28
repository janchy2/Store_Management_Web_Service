import argparse

from authentication_tests import run_authentication_tests
from level0_tests         import run_level0_tests
from level1_tests         import run_level1_tests
from level2_tests         import run_level2_tests
from level3_tests         import run_level3_tests

DELIMITER = "=" * 30

parser = argparse.ArgumentParser (
    description     = "IEP project grading tests",
    formatter_class = argparse.RawTextHelpFormatter
)

parser.add_argument (
        "--authentication-url",
        help = "URL of the authentication container"
)

parser.add_argument (
        "--jwt-secret",
        help = "JWT secret used to encode JWT tokens"
)

parser.add_argument (
        "--roles-field",
        help = "Name of the field used to store role information in JWT token"
)

parser.add_argument (
        "--customer-role",
        help = "Value which represents the customer role"
)

parser.add_argument (
        "--courier-role",
        help = "Value which represents the courier role"
)

parser.add_argument (
        "--owner-role",
        help = "Value which represents the owner role"
)

parser.add_argument (
        "--with-authentication",
        action = "store_true",
        help   = "Value which indicates if requests should include authorization header"
)

parser.add_argument (
        "--customer-url",
        help = "URL of the customer container"
)

parser.add_argument (
        "--courier-url",
        help = "URL of the courier container"
)

parser.add_argument (
        "--owner-url",
        help = "URL of the owner container"
)

parser.add_argument (
        "--with-blockchain",
        action = "store_true",
        help   = "Value which indicates if the testing should include cheking of transactions"
)

parser.add_argument (
        "--provider-url",
        help = "URL used for communication with the blockchain platform"
)

parser.add_argument (
        "--customer-keys-path",
        help = "Path to the customer keys file"
)

parser.add_argument (
        "--customer-passphrase",
        help = "Passphrase usued to decode the customer keys file"
)

parser.add_argument (
        "--owner-private-key",
        help = "Owners private key"
)

parser.add_argument (
        "--courier-private-key",
        help = "Couriers private key"
)

helpText = """ 
Specifies which tests will be run. Value "authentication" runs test which grade authentication endpoints. Following parameters are required:
    --authentication-url
    --jwt-secret
    --roles-field
    --owner-role
    --courier-role
    --customer-role
    
    Example:
    python main.py --type authentication --authentication-url http://127.0.0.1:5000 --jwt-secret JWT_SECRET_DEV_KEY --roles-field roles --owner-role owner --customer-role customer --courier-role courier 

The remainder of the tests are split into levels. Higher level tests will also run lower level tests (if value "level2" is specified, "level0" and "level1" tests will also be included). Following levels are supported:

1) Value "level0" is used for running tests which grade endpoints that update and search products. Following parameters are supported:
    --with-authentication
    --authentication-url
    --owner-url
    --customer-url

    Parameters --owner-url and --customer-url are required. 
    If --with-authentication is present, --authentication-url must also be specified. 
    
    Example:
    python main.py --type level0 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002
    or
    python main.py --type level0 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002
    
2) Value "level1" is used for running tests which grade endpoints that create orders and retrieve order information. Following parameters are supported:
    --with-authentication
    --authentication-url
    --owner-url
    --customer-url
    --with-blockchain 
    --provider-url
    --customer-keys-path
    --customer-passphrase
    --owner-private-key
    
    Parameters --owner-url and --customer-url are required. 
    If --with-authentication is present, --authentication-url must also be specified. Example:
    If --with-blockchain is present, --provider-url, --customer-keys-path, --customer-passphrase and --owner-private-key must also be specified.

    Example:
    python main.py --type level1 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002
    or
    python main.py --type level1 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002
    or
    python main.py --type level1 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --with-blockchain --provider-url http://127.0.0.1:8545 --customer-keys-path ./keys.json --customer-passphrase iep_project --owner-private-key 0xb64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60
    
3) Value "level2" is used for running tests which grade endpoints regarding order pickup and delivery. Following parameters are supported:
    --with-authenti
    cation
    --authentication-url
    --owner-url
    --customer-url
    --courier-url
    --with-blockchain 
    --provider-url
    --customer-keys-path
    --customer-passphrase
    --owner-private-key
    --courier-private-key
    
    Parameters --customer-url and --courier-url are required. 
    If --with-authentication is present, --authentication-url must also be specified. 
    If --with-blockchain is present, --provider-url, --customer-keys-path, --customer-passphrase, --owner-private-key and --courier-private-key must also be supplied.
    
    Example:
    python main.py --type level2 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003
    or
    python main.py --type level2 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003
    or
    python main.py --type level2 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003 --with-blockchain --provider-url http://127.0.0.1:8545 --customer-keys-path ./keys.json --customer-passphrase iep_project --owner-private-key 0xb64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60 --courier-private-key 0xbe07088da4ecd73ecb3d9d806cf391dfaef5f15f9ee131265da8af81728a4379
    
4) Value "level3" is used for running tests which grade endpoints that provide owners with product and category statistics. Following parameters are supported:
    --with-authentication
    --authentication-url
    --customer-url
    --owner-url
    --courier-url
    --with-blockchain 
    --provider-url
    --customer-keys-path
    --customer-passphrase
    --owner-private-key
    --courier-private-key
    
    Parameters --courier-url, --customer-url and --owner-url are required. 
    If --with-authentication is present, --authentication-url must also be supplied. 
    If --with-blockchain is present, --provider-url, --customer-keys-path, --customer-passphrase, --owner-private-key and --courier-private-key must also be supplied.
    
    Example:
    python main.py --type level3 --customer-url http://127.0.0.1:5001 --courier-url http://127.0.0.1:5002 --owner-url http://127.0.0.1:5003
    or
    python main.py --type level3 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003
    or
    python main.py --type level3 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003 --with-blockchain --provider-url http://127.0.0.1:8545 --customer-keys-path ./keys.json --customer-passphrase iep_project --owner-private-key 0xb64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60 --courier-private-key 0xbe07088da4ecd73ecb3d9d806cf391dfaef5f15f9ee131265da8af81728a4379
    
Value "all" is used for running all tests (including authentication). Following parameters are required:
    --authentication-url
    --jwt-secret
    --roles-field
    --courier-role
    --customer-role
    --owner-role
    --owner-url
    --courier-url
    --customer-url
    --with-blockchain 
    --provider-url
    --customer-keys-path
    --customer-passphrase
    --owner-private-key
    --courier-private-key
    
    Example:
    python main.py --type all --authentication-url http://127.0.0.1:5000 --jwt-secret JWT_SECRET_DEV_KEY --roles-field roles --owner-role owner --customer-role customer --courier-role courier --with-authentication --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003
    or
    python main.py --type all --authentication-url http://127.0.0.1:5000 --jwt-secret JWT_SECRET_DEV_KEY --roles-field roles --owner-role owner --customer-role customer --courier-role courier --with-authentication --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003 --with-blockchain --provider-url http://127.0.0.1:8545 --customer-keys-path ./keys.json --customer-passphrase iep_project --owner-private-key 0xb64be88dd6b89facf295f4fd0dda082efcbe95a2bb4478f5ee582b7efe88cf60 --courier-private-key 0xbe07088da4ecd73ecb3d9d806cf391dfaef5f15f9ee131265da8af81728a4379
"""

parser.add_argument (
        "--type",
        required = True,
        choices = ["authentication", "level0", "level1", "level2", "level3", "all"],
        default = "all",
        help = helpText
)


def check_arguments ( arguments, *keys ):
    present = True
    for key in keys:
        if ( key not in arguments ):
            print ( f"Argument {key} is missing." )
            present = False

    return present


AUTHENTICATION = 1.
LEVEL0         = 1.
LEVEL1         = 1.
LEVEL2         = 1.
LEVEL3         = 1.

AUTHENTICATION_FACTOR = 0.1

if (__name__ == "__main__"):
    arguments = parser.parse_args ( )

    total = 0
    max   = 0

    if ( ( arguments.type == "all" ) or ( arguments.type == "authentication" ) ):
        correct = check_arguments (
            vars ( arguments ),
            "authentication_url",
            "jwt_secret",
            "roles_field",
            "customer_role",
            "courier_role",
            "owner_role"
        )

        if ( correct ):
            print ( "RUNNING AUTHENTICATION TESTS" )
            print ( DELIMITER )

            percentage = run_authentication_tests (
                arguments.authentication_url,
                arguments.jwt_secret,
                arguments.roles_field,
                arguments.customer_role,
                arguments.courier_role,
                arguments.owner_role
            )

            authentication_score = AUTHENTICATION * percentage

            total += authentication_score

            
            print ( f"AUTHENTICATION = {authentication_score / AUTHENTICATION * 100:.2f}%" )
            print ( DELIMITER )

    if ( ( arguments.type == "all" ) or ( arguments.type >= "level0" ) ):
        correct = check_arguments (
            vars ( arguments ),
            "courier_url",
            "customer_url"
        )

        if ( arguments.with_authentication ):
            correct &= check_arguments (
                vars ( arguments ),
                "authentication_url"
            )

        if ( correct ):
            print ( "RUNNING LEVEL 0 TESTS" )
            print ( DELIMITER )

            percentage = run_level0_tests (
                arguments.with_authentication,
                arguments.authentication_url,
                arguments.owner_url,
                arguments.customer_url
            )

            level0_score = LEVEL0 * percentage

            if ( not arguments.with_authentication ):
                level0_score *= AUTHENTICATION_FACTOR

            total += level0_score

            print ( f"LEVEL 0 = {level0_score / LEVEL0 * 100:.2f}%" )
            print ( DELIMITER )

    if ( ( arguments.type == "all" ) or ( arguments.type >= "level1" ) ):
        correct = check_arguments (
            vars ( arguments ),
            "customer_url",
            "courier_url"
        )

        if ( arguments.with_authentication ):
            correct &= check_arguments (
                vars ( arguments ),
                "authentication_url"
            )

        if ( arguments.with_blockchain ):
            correct &= check_arguments (
                vars ( arguments ),
                "customer_keys_path",
                "customer_passphrase",
                "owner_private_key",
                "provider_url"
            )

        if ( correct ):
            print ( "RUNNING LEVEL 1 TESTS" )
            print ( DELIMITER )

            percentage = run_level1_tests (
                arguments.with_authentication,
                arguments.authentication_url,
                arguments.customer_url,
                arguments.with_blockchain,
                arguments.customer_keys_path,
                arguments.customer_passphrase,
                arguments.owner_private_key,
                arguments.provider_url
            )

            level1_score = LEVEL1 * percentage

            if ( not arguments.with_authentication ):
                level1_score *= AUTHENTICATION_FACTOR

            total += level1_score

            print ( f"LEVEL 1 = {level1_score / LEVEL1 * 100:.2f}%" )
            print ( DELIMITER )

    if ( ( arguments.type == "all" ) or ( arguments.type >= "level2" ) ):
        correct = check_arguments (
            vars ( arguments ),
            "owner_url",
            "customer_url",
            "courier_url"
        )

        if ( arguments.with_authentication ):
            correct &= check_arguments (
                vars ( arguments ),
                "authentication_url"
            )

        if ( arguments.with_blockchain ):
            correct &= check_arguments (
                vars ( arguments ),
                "owner_private_key",
                "customer_keys_path",
                "customer_passphrase",
                "courier_private_key",
                "provider_url"
            )

        if ( correct ):
            print ( "RUNNING LEVEL 2 TESTS" )
            print ( DELIMITER )

            percentage = run_level2_tests (
                arguments.with_authentication,
                arguments.authentication_url,
                arguments.customer_url,
                arguments.courier_url,
                arguments.with_blockchain,
                arguments.owner_private_key,
                arguments.customer_keys_path,
                arguments.customer_passphrase,
                arguments.courier_private_key,
                arguments.provider_url
            )

            level2_score = LEVEL2 * percentage

            if ( not arguments.with_authentication ):
                level2_score *= AUTHENTICATION_FACTOR

            total += level2_score

            print ( f"LEVEL 2 = {level2_score / LEVEL2 * 100:.2f}%" )
            print ( DELIMITER )

    if ( ( arguments.type == "all" ) or ( arguments.type >= "level3" ) ):
        correct = check_arguments (
            vars ( arguments ),
            "courier_url",
            "customer_url",
            "owner_url",
        )

        if ( arguments.with_authentication ):
            correct &= check_arguments (
                vars ( arguments ),
                "authentication_url"
            )

        if ( arguments.with_blockchain ):
            correct &= check_arguments (
                vars ( arguments ),
                "owner_private_key",
                "customer_keys_path",
                "customer_passphrase",
                "courier_private_key",
                "provider_url"
            )


        if ( correct ):
            print ( "RUNNING LEVEL 3 TESTS" )
            print ( DELIMITER )

            percentage = run_level3_tests (
                arguments.with_authentication,
                arguments.authentication_url,
                arguments.owner_url,
                arguments.customer_url,
                arguments.courier_url,
                arguments.with_blockchain,
                arguments.owner_private_key,
                arguments.customer_keys_path,
                arguments.customer_passphrase,
                arguments.courier_private_key,
                arguments.provider_url
            )

            level3_score = LEVEL3 * percentage

            if ( not arguments.with_authentication ):
                level3_score *= AUTHENTICATION_FACTOR

            total += level3_score

            print ( f"LEVEL 3 = {level3_score / LEVEL3 * 100:.2f}%" )
            print ( DELIMITER )

    max = AUTHENTICATION + LEVEL0 + LEVEL1 + LEVEL2 + LEVEL3
    percentage = total / max * 100
    print ( f"SCORE = {percentage:.2f}%" )
