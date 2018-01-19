from pybitcoin import BitcoinPrivateKey
import sys
import os
import socket


class WalletGen:
    def __init__(self, hostname):
        self.isLinux = sys.platform.lower().startswith('linux')
        self.keyCount = 0
        self.phrases = []
        self.years = []
        self.keys = []
        self.isYearCombo = False

        # Default files
        self.wordFile = 'lastNames.txt'
        self.yearFile = 'years.txt'
        self.fileName = filter(str.isalnum, self.wordFile)

        # Key dump location
        self.dumpFolder = "C:\\bitcon\\"
        if self.isLinux:
            self.dumpFolder = "/var/www/html/"

        if not os.path.exists(self.dumpFolder):
            os.makedirs(self.dumpFolder)

        # Select what to generate based on hostname
        self.genSelector(hostname.lower())

        # Write any leftover keys
        if len(self.keys) > 0:
            self.writeOutKeys()

    def genSelector(self, hostname):
        print("running on {}".format(hostname))

        if 'i3' in hostname:
            self.wordFile = 'femaleFirstNames.txt'
            self.isYearCombo = True

        if 'penti' in hostname:
            self.wordFile = 'maleFirstNames.txt'
            self.isYearCombo = True

        if 'duo2' in hostname:
            self.wordFile = 'lizard.txt'
            self.isYearCombo = False

        if 'bowstaff' in hostname:
            self.wordFile = 'lastNames.txt'
            self.isYearCombo = False

        self.fileName = filter(str.isalnum, self.wordFile)

        if self.isYearCombo:
            self.fileName = filter(str.isalnum, self.wordFile + self.yearFile)
            self.loadYears()

        self.fileName = "{}_{}".format(hostname, self.fileName.replace('txt', ''))

        if 'names' in self.fileName.lower():
            self.loadNames()
            if self.isYearCombo:
                self.generateNameYearWallets()
            else:
                self.generatePhraseWallets()
        else:
            self.loadPhrases()
            self.generatePhraseWallets()

    def generatePhraseWallets(self):
        for phrase in self.phrases:
            private_key = BitcoinPrivateKey.from_passphrase(phrase)
            self.keys.append(private_key.to_wif())
            self.keyCount += 1
            if self.keyCount % 5 == 0:
                self.writeOutKeys()
                self.keys = []

    def generateNameYearWallets(self):
        for name in self.phrases:
            for year in self.years:
                # Name Title Case
                phrase = "{}{}".format(name, year)
                private_key = BitcoinPrivateKey.from_passphrase(phrase)
                self.keys.append(private_key.to_wif())
                self.keyCount += 1

                # Name lower Case
                phrase = phrase.lower()
                private_key = BitcoinPrivateKey.from_passphrase(phrase)
                self.keys.append(private_key.to_wif())
                self.keyCount += 1

                if self.keyCount % 5000 == 0:
                    self.writeOutKeys()
                    self.keys = []

    def writeOutKeys(self):
        fName = "{}_{}.txt".format(self.fileName, self.keyCount)
        fileName = "{}{}".format(self.dumpFolder, fName)

        with open(fileName, 'a') as the_file:
            for aKey in self.keys:
                the_file.write(aKey + '\n')

    def loadPhrases(self):
        with open(self.wordFile) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        for line in content:
            self.phrases.append(line)

    def loadNames(self):
        with open(self.wordFile) as f:
            content = f.readlines()

        content = [x.strip() for x in content]
        for line in content:
            name = line.split(' ')[0]
            self.phrases.append(name.title())

    def loadYears(self):
        with open(self.yearFile) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        for line in content:
            self.years.append(line)


def main():
    WalletGen(socket.gethostname())


if __name__ == '__main__':
    main()
