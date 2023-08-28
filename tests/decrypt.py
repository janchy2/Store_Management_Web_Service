from web3 import Account
import os

script_dir = os.path.dirname(__file__)

keys_file_path = os.path.join(script_dir, "keys.json")

with open (keys_file_path, "r" ) as file:
    private_key = Account.decrypt ( file.read ( ), "iep_project" ).hex ( )
    print(private_key)
