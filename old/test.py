from pybitcoin import BitcoinPrivateKey
import sys
import os
import socket


class WalletGen:
    def __init__(self):
        self.isLinux = sys.platform.lower().startswith('linux')
        self.keyCount = 0
        self.phrases = []
        self.years = []
        self.keys = []

        # Default files
        self.wordFile = 'lastNames.txt'
        self.yearFile = 'years.txt'
        self.fileName = filter(str.isalnum, self.wordFile)

        # Key dump location
        self.dumpFolder = "C:\\bitcon\\lastNames\\"
        if self.isLinux:
            self.dumpFolder = "/var/www/html/lastNames//"

        if not os.path.exists(self.dumpFolder):
            os.makedirs(self.dumpFolder)

        # Select what to generate based on hostname
        self.genSelector()

        # Write any leftover keys
        if len(self.keys) > 0:
            self.writeOutKeys()


    def genSelector(self):
        self.fileName = "{}".format(self.fileName.replace('txt', ''))
        print("generating {}".format(self.fileName))

        self.loadYears()
        self.loadNames()
        # print(len(self.phrases))
        self.generatePhraseWallets()


    def loadYears(self):
        with open(self.yearFile) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        for line in content:
            self.years.append(line)


    def loadNames(self):
        with open(self.wordFile) as f:
            content = f.readlines()

        content = [x.strip() for x in content]
        for line in content:
            name = line.split(' ')[0].lower()

            self.phrases.append(name.title())
            self.phrases.append(name.lower())

            for year in self.years:
                self.phrases.append("{}{}".format(name.title(), year))
                self.phrases.append("{}{}".format(name.lower(), year))


    def loadTeamPhrases(self):
        with open(self.wordFile) as f:
            content = f.readlines()
        content = [x.strip() for x in content]

        for line in content:
            lineArrayLower = [x.strip().lower() for x in line.split(" ")]
            lineArrayTitle = [x.title() for x in lineArrayLower]

            fullStringLower = ''.join(lineArrayLower)
            fullStringTitle = ''.join(lineArrayTitle)

            teamNameLower = lineArrayLower[len(lineArrayLower)-1]
            teamNameTitle = lineArrayTitle[len(lineArrayTitle)-1]

            if '49Ers' in fullStringTitle:
                fullStringTitle = fullStringTitle.replace('Ers', 'ers')

            self.phrases.append(fullStringLower)
            self.phrases.append(fullStringTitle)

            if '49Ers' not in teamNameTitle:
                teamNameTitle = teamNameTitle.replace('Ers', 'ers')
                self.phrases.append(teamNameTitle)

            self.phrases.append(teamNameLower)

            for year in self.years:
                self.phrases.append("{}{}".format(fullStringLower,year))
                self.phrases.append("{}{}".format(fullStringTitle,year))
                self.phrases.append("{}{}".format(teamNameLower, year))
                if '49Ers' not in teamNameTitle:
                    self.phrases.append("{}{}".format(teamNameTitle, year))

    def generatePhraseWallets(self):
        for phrase in self.phrases:
            private_key = BitcoinPrivateKey.from_passphrase(phrase)
            wif = private_key.to_wif()
            self.keys.append(wif)
            self.keyCount += 1
            if self.keyCount % 5000 == 0:
                print("Writing out: {}".format(self.keyCount))
                self.writeOutKeys()
                self.keys = []


    def writeOutKeys(self):
        fName = "{}_{}.txt".format(self.fileName, self.keyCount)
        fileName = "{}{}".format(self.dumpFolder, fName)

        with open(fileName, 'a') as the_file:
            for aKey in self.keys:
                the_file.write(aKey + '\n')


def main():
    WalletGen()


if __name__ == '__main__':
    main()
