import BitcoinUtils
import FileUtils
import logging
import datetime


class BitGen:
    def __init__(self, bitcoinWalLoc, walletBackLoc, keyFilesLoc):
        self.setupLogging()

        # Utils for working with bitcoind
        self.bitcoind = BitcoinUtils.BUtils()

        # Utils for reading, writing, moving key files and wallets.
        self.fileUtils = FileUtils.FUtils(bitcoinWalLoc, walletBackLoc, keyFilesLoc)

        # A list of all key files in a directory.
        self.keyFiles = self.fileUtils.keyFiles()

        if len(self.keyFiles) > 0:
            logging.info("{} Keyfiles Loaded #:{}".format(datetime.datetime.now(), len(self.keyFiles)))
        else:
            logging.error("{} NO KEY FILES FOUND #:{}".format(datetime.datetime.now(), len(self.keyFiles)))

        self.run()

    def run(self):
        if self.bitcoind.isRunning():
            logging.info("{} Stopping previous bitcoind session.".format(datetime.datetime.now()))
            self.bitcoind.stop()
            self.fileUtils.backupWallet()

        self.bitcoind.start()
        logging.info("{} bitcoind started.".format(datetime.datetime.now()))

        for keyfile in self.keyFiles:
            keyList = self.fileUtils.keyList(keyfile)
            logging.info("{} Importing Keys ({}) from {}".format(datetime.datetime.now(), len(keyList), keyfile))

            # IMPORT
            importCount = 0
            walletName = "wall"
            for key in keyList:
                importCount += 1

                if importCount % 100 == 0:
                    walletName = "wall" + str(importCount)
                    logging.info("{} Importing to wallet {}".format(datetime.datetime.now(), walletName))

                self.bitcoind.importKey(key, walletName)

            # Rescan and Backup
            logging.info("{} Stopping bitcoind session for rescan".format(datetime.datetime.now()))
            self.bitcoind.stop()
            logging.info("{} Rescanning".format(datetime.datetime.now()))
            self.bitcoind.start(True)

            fname = keyfile.split('/')[len(keyfile.split('/')) - 1].replace(".txt", '')
            accountList = self.bitcoind.listAccounts()
            logging.info("{} Results from {} --- {}".format(datetime.datetime.now(), keyfile, accountList))
            self.bitcoind.stop()

            logging.info("{} Backing Up Wallet".format(datetime.datetime.now()))
            self.fileUtils.backupWallet(fname)
            self.bitcoind.start()

    @staticmethod
    def setupLogging():
        logfile = '/home/zebub/bitgenLogs/log.txt'
        logging.basicConfig(filename=logfile, level=logging.INFO)
        logging.info("{} Bitgen Started".format(datetime.datetime.now()))


if __name__ == '__main__':
    BitGen("/home/zebub/.bitcoin/", "/home/zebub/walletBackup/", "/home/zebub/code/keysRepo/")
