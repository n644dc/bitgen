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
        # self.wordFile = 'top100k.txt'
        # self.wordFile = 'topMillion.txt'

        self.folderName = filter(str.isalnum, self.wordFile)

        # Init Vars
        self.workDir = '/var/www/html/bitcon' if self.isLinux else 'C:\\bitcon'
        self.walletsLoc = "{}/{}/".format(self.workDir, self.folderName) if self.isLinux else "{}\\{}\\".format(
            self.workDir, self.folderName)

        self.logfile = "{}/loggo.txt".format(self.workDir) if self.isLinux else "{}\\loggo.txt".format(self.workDir)

        self.walletsTotalCount = 347500
        self.lastWalletCount = 1
        self.walFileSize = 100
        self.walFolderSize = 20000

        self.Wallets = []
        self.words = []
        self.numbers = []
        self.passwords = []

        # Create DIR Struct
        if not os.path.exists(self.workDir):
            os.makedirs(self.workDir)

        if not os.path.exists(self.walletsLoc):
            os.makedirs(self.walletsLoc)

        logging.basicConfig(filename=self.logfile, level=logging.INFO)

        logging.info("{} Starting At Wallet #: {}".format(datetime.datetime.now(), self.walletsTotalCount))

        if self.walletsTotalCount > 0:
            # Creats folder where we left off if the app is restarted and walletsTotalCount is manually set.
            self.currentWalletFolder = "{}{}_{}".format(self.walletsLoc, self.walletsTotalCount + 1,
                                                        self.walletsTotalCount + 1 + self.walFolderSize)
        else:
            # Basecase starting folder
            self.currentWalletFolder = "{}{}_{}".format(self.walletsLoc, self.lastWalletCount, self.walFolderSize)

    @staticmethod
    def representsInt(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def saveWallets(self):
        currentNumOfWallets = len(self.Wallets)
        if currentNumOfWallets == self.walFileSize:
            fileNom = "{}_{}.txt".format((self.walletsTotalCount - currentNumOfWallets) + 1, self.walletsTotalCount)
            walletFile = "{}/{}".format(self.currentWalletFolder, fileNom) if self.isLinux else "{}\\{}".format(
                self.currentWalletFolder, fileNom)

            if not os.path.exists(self.currentWalletFolder):
                os.makedirs(self.currentWalletFolder)

            with open(walletFile, "w") as savFile:
                for wallet in self.Wallets:
                    line = "{}\n".format(", ".join(wallet))
                    savFile.write(line)

            print("FileSaved: {}".format(walletFile))
            logging.info("{} FileSaved: {}".format(datetime.datetime.now(), walletFile))
            self.Wallets = []

            # If we've reached the wallet folder size, create the next folder
            if self.walletsTotalCount % self.walFolderSize == 0:
                self.lastWalletCount = self.walletsTotalCount + 1
                walletFolderName = "{}_{}".format(self.lastWalletCount, self.walletsTotalCount + self.walFolderSize)
                self.currentWalletFolder = "{}{}".format(self.walletsLoc, walletFolderName)

    def genPrep(self, phraseArray):
        phrase = "".join(phraseArray)
        self.generateWallet(phrase)

    def generateWallet(self, phrase):
        private_key = BitcoinPrivateKey.from_passphrase(phrase)
        phrase = private_key.passphrase()
        privateHex = private_key.to_hex()
        privateWIF = private_key.to_wif()

        public_key = private_key.public_key()
        publicHex = public_key.to_hex()
        publicAddr = public_key.address()
        publicH160 = public_key.hash160()

        wallet = [str(self.walletsTotalCount), phrase, privateHex, privateWIF, publicHex, publicAddr, publicH160]
        self.Wallets.append(wallet)
        self.walletsTotalCount += 1
        self.saveWallets()

    # Manipulate generatePhrases to a desired scheme.
    # Different passphrase schemes will require different generation techniques.
    # Also make sure to adjust startPos to work accordingly when the application/server/etc goes down.
    def generatePhrases(self):
        # with open(self.wordFile) as f:
        #     self.words = f.readlines()
        # self.words = [x.strip() for x in self.words]
        #
        # for word in self.words[self.walletsTotalCount:]:
        #     self.generateWallet(word)

        with open(self.wordFile) as f:
            self.words = f.readlines()

        self.words = [x.strip() for x in self.words]
        self.numbers = [x for x in self.words if self.representsInt(x) and 1900 <= int(x) <= 2020]
        self.words = [x for x in self.words if 4 <= len(x) <= 9]
        self.words = [x for x in self.words if "'" not in x]
        self.words = [x for x in self.words if not self.representsInt(x)]

        regex = re.compile(r'(.)\1{2,}')
        exclude = filter(regex.search, self.words)
        self.words = [x.lower() for x in self.words if x not in exclude]


        # startPos = self.walletsTotalCount  # Use when using a single list and not concating any words or nums together
        startPos = (self.walletsTotalCount / len(self.numbers)) + 1

        for word in self.words[startPos:]:
            for number in self.numbers:
                self.genPrep([word, number])


def main():
    # read in list
    # start recording word combos separate by comma
    # create 100k entries per file

    generator = WalletGen()
    generator.generatePhrases()


if __name__ == '__main__':
    main()
