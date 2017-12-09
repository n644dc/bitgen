from pybitcoin import BitcoinPrivateKey
import sys
import os


class WalletGen:
    def __init__(self):

        isLinux = sys.platform.lower().startswith('linux')

        # Init Vars
        self.workDir = '/var/www/html/bitcon' if isLinux else 'C:\\bitcon'
        self.phraseLocation = "{}/phrases/".format(self.workDir) if isLinux else "{}\\phrases\\".format(self.workDir)
        self.wordFile = 'linux.words'
        self.Phrases = []
        self.Wallets = []
        self.words = []

        # Create DIR Struct
        if not os.path.exists(self.workDir):
            os.makedirs(self.workDir)

        if not os.path.exists(self.phraseLocation):
            os.makedirs(self.phraseLocation)


    def generateWallet(self, phrase):
        # Save Phrase
        self.Phrases.append(phrase)

        private_key = BitcoinPrivateKey.from_passphrase("AA")
        print(private_key.passphrase())
        private_key.to_hex()
        priv2 = BitcoinPrivateKey.from_passphrase(private_key.passphrase())
        areSame = private_key.to_hex() == priv2.to_hex()
        print(areSame)


    def generatePhrases(self):
        with open(self.wordFile) as f:
            self.words = f.readlines()

        self.words = [x.strip() for x in self.words]

        for word in self.words:
            phrase = [].append(word)
            self.generateWallet(phrase)


def main():
    # read in list
    # start recording word combos separate by comma
    # create 100k entries per file

    generator = WalletGen()
    generator.generatePhrases()


if __name__ == '__main__':
    main()
