from web3 import Web3
import json

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

web3.eth.defaultAccount = web3.eth.accounts[0]

abi = json.loads('[{"constant":true,"inputs":[],"name":"getBalance","outputs":[{"name":"","type":"int256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"amt","type":"int256"}],"name":"deposite","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amt","type":"int256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
bitecode = '608060405234801561001057600080fd5b506001600081905550610125806100286000396000f3006080604052600436106053576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806312065fe0146058578063314ec99f1460805780637e62eab81460aa575b600080fd5b348015606357600080fd5b50606a60d4565b6040518082815260200191505060405180910390f35b348015608b57600080fd5b5060a86004803603810190808035906020019092919050505060dd565b005b34801560b557600080fd5b5060d26004803603810190808035906020019092919050505060eb565b005b60008054905090565b806000540160008190555050565b8060005403600081905550505600a165627a7a72305820fd9abb8e503093832babfa7e3c71cf41fe88cab1fe9b58e50bba359d0af80afd0029'

contract = web3.eth.contract(abi=abi,bitecode=bitecode)
tx_hash = contract.constructor().transact()

tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
print(tx_receipt)

contract = web3.eth.contract(
	address=tx_receipt.contractAddress,
	abi=abi
	)
print(contract.functions.getBalance().call())

tx_hash = contract.functions.withdraw(1).transact()
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
print(contract.functions.getBalance().call())