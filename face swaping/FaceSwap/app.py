from web3 import Web3

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

account1 = "0xcCac709604495979A81d722a1221c02B07f584DF"
account2 = "0xF5d888009170F040f3DB269f80A1884ED114615C"

private_key = "ab87fc04db548d60ad48de273d6916e6859bc1ef80b319d0dcff3bf40c5695ae"

nonce = web3.eth.getTransactionCount(account1)

tx = {
	'nonce': nonce,
	'to': account2,
	'value': web3.toWei(1,'ether'),
	'gas': 20000000,
	'gasPrice': web3.toWei('50','gwei')
}
signed_tx = web3.eth.account.signTransaction(tx,private_key)
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(web3.toHex(tx_hash))