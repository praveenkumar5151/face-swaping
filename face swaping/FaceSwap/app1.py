from web3 import Web3
import json

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

web3.eth.defaultAccount = web3.eth.accounts[0]

abi = json.loads([{"constant":true,"inputs":[],"name":"getBalance","outputs":[{"name":"","type":"int256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"amt","type":"int256"}],"name":"deposite","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amt","type":"int256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
address = web3.toChecksumAddress("0x5964D88Ad5d3dfdC6340aBB753a9d993aaa3d488")

contract = web3.eth.contract(address=address,abi=abi)

print(contract.functions.getBalance().call())

tx_hash = contract.functions.withdraw(1).transact()

web3.eth.waitTransactionReceipt(tx_hash)

