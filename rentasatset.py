from web3 import HTTPProvider
from web3 import Web3
from eth_abi import encode
from decimal import Decimal
import json
import time
import random
import requests
import schedule

# Koneksi ke Web3
web3 = Web3(Web3.HTTPProvider("https://rpc-bluetail.renta.network"))  # Pastikan ini sebelum `web3.is_connected()`

if web3.is_connected():
    print("Web3 Connected...\n")
else:
    print("Error Connecting. Please Try Again. Exiting...")
    exit()

def tap_onchain(sender, key):
    try:
        gas_price = web3.eth.gas_price / 10**9  # Convert Wei to Gwei
        print(f"Current Gas Price: {gas_price} Gwei")

        if gas_price < 2.5:
            nonce = web3.eth.get_transaction_count(sender)
            tapaddr = web3.to_checksum_address('0x3280E2F59536991B5726B41B9bEEd613B1E0Be0A')
            data = '0xf482ee72'

            gas_amount = web3.eth.estimate_gas({
                'chainId': chainId,
                'from': sender,
                'to': tapaddr,
                'data': data,
                'gasPrice': int(gas_price * 30**9),
                'nonce': nonce
            })

            tap_tx = {
                'chainId': chainId,
                'from': sender,
                'to': tapaddr,
                'data': data,
                'gas': gas_amount,
                'gasPrice': int(gas_price * 30**9),
                'nonce': nonce
            }

            # Sign and send the transaction
            signed_tx = web3.eth.account.sign_transaction(tap_tx, key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f'For Address {sender}')
            print(f'Processing Tap Onchain...')
            web3.eth.wait_for_transaction_receipt(tx_hash)
            print(f'Tap Onchain Success!')
            print(f'TX-ID : {str(web3.to_hex(tx_hash))}')
        else:
            print("Gas price too high, skipping transaction.")
    except Exception as e:
        print(f"Error: {e}")
        pass

def main():
    while True:
        with open('pvkeylist.txt', 'r') as file:
            local_data = file.read().splitlines()
            for pvkey in local_data:
                sender = web3.eth.account.from_key(pvkey)
                tap_onchain(sender.address, pvkey)
        print("Waiting for 120 seconds before the next cycle...")
        time.sleep(120)

if __name__ == "__main__":
    main()
