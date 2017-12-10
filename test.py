from pybitcoin import BitcoinPrivateKey
import sys
import os


class WalletGen:
    def __init__(self):

        self.isLinux = sys.platform.lower().startswith('linux')

        # Init Vars
        self.wordFile = 'linux.words'
        # self.passwords = 'top100k.txt'
        self.passwordsFile = 'topMillion.txt'
        self.walletsTotalCount = 0
        self.words = []
        self.numbers = []


    @staticmethod
    def representsInt(s):
        try:
            int(s)
            return True
        except ValueError:
            return False


    def genPrep(self, phraseArray):
        # Prase with spaces
        phrase = " ".join(phraseArray)
        self.generateWallet(phrase)


    def generateWallet(self, phrase):
        private_key = BitcoinPrivateKey.from_passphrase(phrase)
        phrase = private_key.passphrase()
        privateHex = private_key.to_hex()
        privateWIF = private_key.to_wif()

        public_key = private_key.public_key()
        publicHex  = public_key.to_hex()
        publicAddr = public_key.address()
        publicH160 = public_key.hash160()

        wallet = [phrase, privateHex, privateWIF, publicHex, publicAddr, publicH160]
        print("Wallet Created: {}".format(wallet))
        self.walletsTotalCount += 1

    def generatePhrases(self):
        with open(self.passwordsFile) as f:
            self.words = f.readlines()

        with open(self.wordFile) as f:
            self.words = f.readlines()

        # self.words = [x.strip() for x in self.words]
        # self.numbers = [x for x in self.words if self.representsInt(x)]
        # self.words = [x for x in self.words if len(x) >= 3]
        # self.words = [x for x in self.words if "'" not in x]
        # self.words = self.words + self.numbers
        #
        # for word in self.words:
        #     self.genPrep([word])
        #     for number in self.numbers:
        #         self.genPrep([word, number])



def main():
    # read in list
    # start recording word combos separate by comma
    # create 100k entries per file

    generator = WalletGen()
    generator.generatePhrases()


if __name__ == '__main__':
    main()
