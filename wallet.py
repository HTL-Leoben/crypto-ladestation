from bitcoinlib.wallets import Wallet

wallet = Wallet.create('Bezahlautomat_Fach1', network='testnet')
key = wallet.get_key()
print("Adresse:", key.address)
print("Private Key (WIF):", key.wif)