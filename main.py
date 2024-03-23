# Public key & Private key account
sender_address = "XXX WALLET"
sender_key = "XXX PRIVKEY"
recipient_address = "XXX WALLET"

# infura apikey
infura_apikey = "apikey"
infura_url= f"https://goerli.infura.io/v3/e3a353ba9d1b4c4299512af80277f4e5"

# Ganache Testnet
ganache_mode = False
ganache_url = "HTTP://127.0.0.1:8545"


# import libraries
from decimal import *
from web3 import Web3

if ganache_mode:
    web3 = Web3(Web3.HTTPProvider(ganache_url))
else:
    web3 = Web3(Web3.HTTPProvider(infura_url))

# check connecting web3 to Ganache
if  web3.is_connected() != True:
    print("ERROR, connecting web3...")
    exit()

# set gas fee
gasLimit = 21000
gasPrice = 15
gas_fee = web3.from_wei(Decimal(gasLimit * gasPrice), 'ether')
print("gas fee:", gas_fee)

# get balance
balance = web3.eth.get_balance(sender_address)
balance = web3.from_wei(balance, "ether")
print("balance:", balance)

# check balance
amount = Decimal(0.0001)
assert balance >= gas_fee + amount, "Error, Not enough balance"

# get nonce number
nonce = web3.eth.get_transaction_count(sender_address)

# build transaction
tx = {
    'nonce': nonce,
    'to': recipient_address,
    'value': web3.to_wei(amount, 'ether'),
    'gas': gasLimit,
    'gasPrice': gasPrice
}
print(tx)
signed_tx = web3.eth.account.sign_transaction(tx, sender_key)
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
print("Transaction Completed:", web3.to_hex(tx_hash))