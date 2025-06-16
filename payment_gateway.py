
import requests
import time

TESTNET_BASE_URL = "https://mempool.space/testnet/api"
TESTNET_ADDRESS = "tb1qs3kmklxt8g4dnf45zf5qdcn9tljyse5l6skcks"  # z. B. tb1q....

last_seen_txids = set()
 
def check_new_transactions():
    url = f"{TESTNET_BASE_URL}/address/{TESTNET_ADDRESS}/txs"
    response = requests.get(url)

    if response.status_code != 200:
        print("Fehler beim Abrufen der Transaktionen:", response.text)
        return

    txs = response.json()

    for tx in txs:
        txid = tx["txid"]
        if txid not in last_seen_txids:
            print(f"Neue Transaktion erkannt: {txid}")
            on_new_payment(tx)
            last_seen_txids.add(txid)

def convertBtcToEur(btc_value):

    # Hole aktuellen BTC/EUR Kurs
    price_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur"
    r = requests.get(price_url)
    if r.status_code == 200:
        btc_eur = r.json()["bitcoin"]["eur"]
        value_eur = btc_value * btc_eur
        return value_eur;
    else:
        print(f"Empfangen: {btc_value:.8f} BTC (Kurs konnte nicht geladen werden)")
        return 0;

def on_new_payment(tx_data):
    print("💰 Neue Zahlung eingegangen!")

    # Gehe durch alle Outputs und finde den Betrag an unsere Adresse
    for vout in tx_data['vout']:
        address = vout.get('scriptpubkey_address')
        value_sats = vout.get('value', 0)

        btc_value = value_sats / 1e8  # Satoshi → BTC
        eur_value = convertBtcToEur(btc_value)

        print(f"Empfangen: {eur_value:.2f} € ")

# Polling-Loop starten
if __name__ == "__main__":
    print("Überwache Adresse:", TESTNET_ADDRESS)
    while True:
        check_new_transactions()
        time.sleep(10)  # alle 30 Sekunden prüfen

