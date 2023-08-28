from web3 import Web3
from web3 import HTTPProvider 
from web3 import Account


private_key = ""
with open ( "keys.json", "r" ) as file:
    private_key = Account.decrypt ( file.read ( ), "iep_project" ).hex ( )

customer_account = Account.from_key ( private_key )

web3 = Web3 ( HTTPProvider ( "http://127.0.0.1:8545" ) )

result = web3.eth.send_transaction ({
    "from": web3.eth.accounts[0],
    "to": customer_account.address,
    "value": web3.to_wei ( 2, "ether" )
})
