from web3 import Web3, HTTPProvider
from eth_abi import encode
from decimal import Decimal
import json
import time
import random
import requests
import schedule

web3 = Web3(Web3.HTTPProvider("https://rpc-bluetail.renta.network/3v8YuduEcfihmCBksL8U1W98mXbyY7vDv"))
chainId = web3.eth.chain_id

# Connecting to Web3
if web3.is_connected():
    print("Web3 Connected...\n")
else:
    print("Error Connecting. Please Try Again. Exiting...")
    exit()

def tapOnchain(sender, key):
    try:
        gasPrice = web3.eth.gas_price
        nonce = web3.eth.get_transaction_count(sender)
        tapaddr = web3.to_checksum_address('0x53A389E93e2764037c80E0C04eeBef45b4387992')
        data = '0xfd221031'

        gasAmount = web3.eth.estimate_gas({
            'chainId': chainId,
            'from': sender,
            'to': tapaddr,
            'data': data,
            'gasPrice': gasPrice,
            'nonce': nonce
        })

        tap_tx = {
            'chainId': chainId,
            'from': sender,
            'to': tapaddr,
            'data': data,
            'gas': gasAmount,
            'gasPrice': gasPrice,
            'nonce': nonce
        }
        
        # Sign and send the transaction
        tx_hash = web3.eth.send_raw_transaction(web3.eth.account.sign_transaction(tap_tx, key).rawTransaction)
        # Get transaction hash
        print(f'For Address {sender}')
        print(f'Processing Tap Onchain...')
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f'Tap Onchain Success!')
        print(f'TX-ID : {str(web3.to_hex(tx_hash))}')
    except Exception as e:
        print(f"Error: {e}")
        pass

def process_private_keys():
    with open('pvkeylist.txt', 'r') as file:
        local_data = file.read().splitlines()
        for pvkeylist in local_data:
            sender = web3.eth.account.from_key(pvkeylist)
            for _ in range(15):  # Loop 15 times for each private key
                tapOnchain(sender.address, sender.key)
                time.sleep(1)  # Optional: Add a delay between transactions

# Schedule the task to run every 3 hours
schedule.every(3).hours.do(process_private_keys)

print("Scheduler started. The task will run every 3 hours.")
while True:
    schedule.run_pending()
    time.sleep(1)