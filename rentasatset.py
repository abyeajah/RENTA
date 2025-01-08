from web3 import HTTPProvider
from web3 import Web3
from decimal import Decimal
import time

# Koneksi ke Web3
web3 = Web3(Web3.HTTPProvider("https://rpc-bluetail.renta.network"))  # Pastikan URL RPC benar

if web3.is_connected():
    print("Web3 Connected...\n")
else:
    print("Error Connecting. Please Try Again. Exiting...")
    exit()

# Definisi chainId (pastikan sesuai dengan jaringan Anda)
chainId = web3.eth.chain_id  # Mengambil chain ID dari jaringan

def tap_onchain(sender, key):
    try:
        # Ambil Gas Price
        gas_price_wei = web3.eth.gas_price
        gas_price_gwei = gas_price_wei / 10**9

        # Batas maksimal gas price
        MAX_GAS_PRICE = 5.0  # Gwei

        # Tampilkan informasi gas price
        print(f"Current Gas Price: {gas_price_gwei:.8f} Gwei")

        # Periksa apakah gas price memenuhi syarat transaksi
        if gas_price_gwei < 0.05:
            print("Gas price too low, skipping transaction to save cost.\n")
            return
        elif gas_price_gwei > MAX_GAS_PRICE:
            print(f"Gas price exceeds the limit of {MAX_GAS_PRICE} Gwei, skipping transaction.\n")
            return

        # Lanjutkan transaksi jika gas price sesuai
        nonce = web3.eth.get_transaction_count(sender)
        tapaddr = web3.to_checksum_address('0x3280E2F59536991B5726B41B9bEEd613B1E0Be0A')
        data = '0xf482ee72'

        gas_amount = web3.eth.estimate_gas({
            'chainId': chainId,
            'from': sender,
            'to': tapaddr,
            'data': data,
            'gasPrice': gas_price_wei,
            'nonce': nonce
        })

        # Buat transaksi
        tap_tx = {
            'chainId': chainId,
            'from': sender,
            'to': tapaddr,
            'data': data,
            'gas': gas_amount,
            'gasPrice': gas_price_wei,
            'nonce': nonce
        }

        # Tanda tangan dan kirim transaksi
        signed_tx = web3.eth.account.sign_transaction(tap_tx, key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f'For Address {sender}')
        print(f'Processing Tap Onchain...')
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f'Tap Onchain Success!')
        print(f'TX-ID : {str(web3.to_hex(tx_hash))}')
    except Exception as e:
        print(f"Error: {e}")
        pass

def main():
   
