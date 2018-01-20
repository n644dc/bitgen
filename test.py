from pybitcoin import BitcoinPrivateKey
import sys
import os


phrase = "sheep answer taint song party trouble confuse very next shown mumble team 1989"
private_key = BitcoinPrivateKey.from_passphrase(phrase)
print private_key.to_wif()