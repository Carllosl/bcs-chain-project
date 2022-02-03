import json
import requests
from pycoin.networks.bitcoinish import create_bitcoinish_network
from pycoin.coins.bitcoin.Tx import Spendable
from pycoin.coins.tx_utils import create_tx
from pycoin.encoding.hexbytes import h2b
from pycoin.solve.utils import build_hash160_lookup
from pycoin.ecdsa.secp256k1 import secp256k1_generator
from . import settings_my


def get_address(method, params=[]):
    payload = json.dumps({
        "method": method,
        "params": params
    })
    return requests.post(settings_my.url, auth=(settings_my.user, settings_my.password), data=payload).json()['result']

def send_trans(tx=[]):
    payload = json.dumps({
        "method": 'sendrawtransaction',
        "params": tx
    })
    return requests.post(settings_my.url, auth=(settings_my.user, settings_my.password), data=payload).json()

def new_trans():
    network = create_bitcoinish_network(symbol='', network_name='', subnet_name='',
                                        wif_prefix_hex="80", address_prefix_hex="19",
                                        pay_to_script_prefix_hex="32", bip32_prv_prefix_hex="0488ade4",
                                        bip32_pub_prefix_hex="0488B21E", bech32_hrp="bc",
                                        bip49_prv_prefix_hex="049d7878",
                                        bip49_pub_prefix_hex="049D7CB2", bip84_prv_prefix_hex="04b2430c",
                                        bip84_pub_prefix_hex="04B24746", magic_header_hex="F1CFA6D3", default_port=3666)
    address_from = settings_my.address_from
    utxo = requests.get(f'https://bcschain.info/api/address/{address_from}/utxo')
    utxo = json.loads(utxo.text)[0]
    address_to = get_address("getnewaddress")
    spendables = Spendable(coin_value=int(utxo['value']), script=h2b(utxo['scriptPubKey']),
                                    tx_hash=h2b(utxo['transactionId']), tx_out_index=int(utxo['outputIndex']))
    unsigned_tx = create_tx(
        network = network,
        spendables = [spendables],
        payables=[tuple([address_to, 100000000])],
        fee='standard'
    )
    unsigned_tx_hex = unsigned_tx.as_hex()
    key_wif = network.parse.wif(settings_my.secret_key)
    exponent = key_wif.secret_exponent()
    solver = build_hash160_lookup([exponent], [secp256k1_generator])

    signed_tx = unsigned_tx.sign(solver)
    signed_tx_hex = signed_tx.as_hex()

    trans_id = send_trans([signed_tx_hex])
    return trans_id