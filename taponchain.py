from web3 import Web3, HTTPProvider
from eth_abi import encode
from decimal import Decimal
import json
import time
import random
import requests

web3 = Web3(Web3.HTTPProvider("https://rpc-bluetail.renta.network/3v8YuduEcfihmCBksL8U1W98mXbyY7vDv"))
chainId = web3.eth.chain_id

#connecting web3
if  web3.is_connected() == True:
    print("Web3 Connected...\n")
else:
    print("Error Connecting Please Try Again Exit...")
    exit()

sender = web3.eth.account.from_key(input('input pvkey renta : '))
def tapOnchain():
    try:
        gasPrice = web3.eth.gas_price
        nonce = web3.eth.get_transaction_count(sender.address)
        tapaddr = web3.to_checksum_address('0x53A389E93e2764037c80E0C04eeBef45b4387992')
        data = '0xfd221031'

        gasAmount = web3.eth.estimate_gas({
            'chainId': chainId,
            'from': sender.address,
            'to': tapaddr,
            'data': data,
            'gasPrice': gasPrice,
            'nonce': nonce
        })

        tap_tx = {
            'chainId': chainId,
            'from': sender.address,
            'to': tapaddr,
            'data': data,
            'gas': gasAmount,
            'gasPrice': gasPrice,
            'nonce': nonce
        }
        
        #sign & send the transaction
        tx_hash = web3.eth.send_raw_transaction(web3.eth.account.sign_transaction(tap_tx, sender.key).rawTransaction)
        #get transaction hash
        print(f'Processing Tap Onchain...')
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f'Tap Onchain Success!')
        print(f'TX-ID : {str(web3.to_hex(tx_hash))}')
    except Exception as e:
        print(f"Error: {e}")
        pass

while True:
    tapOnchain()