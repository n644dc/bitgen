from pybitcoin import BitcoinPrivateKey
import sys
import os
import logging
import datetime
import re


class WalletGen:
    def __init__(self):
        self.isLinux = sys.platform.lower().startswith('linux')
        self.wordFile = 'linux.words'

    def generateWallet(self, phrase):
        private_key = BitcoinPrivateKey.from_passphrase(phrase)
        phrase = private_key.passphrase()
        privateHex = private_key.to_hex()
        privateWIF = private_key.to_wif()

        public_key = private_key.public_key()
        publicHex = public_key.to_hex()
        publicAddr = public_key.address()
        publicH160 = public_key.hash160()

        print("Phrase: {}".format(phrase))
        print
        print("PrivateKey HEX: {}".format(privateHex))
        print
        print("PrivateKey WIF: {}".format(privateWIF))
        print
        print
        print
        print("PublicKey HEX: {}".format(publicHex))
        print
        print("PublicKey Address: {}".format(publicAddr))
        print
        print("PublicKey H160 {}".format(publicH160))
        print




def main():
    # read in list
    # start recording word combos separate by comma
    # create 100k entries per file

    generator = WalletGen()
    generator.generateWallet("abc123")


if __name__ == '__main__':
    main()
