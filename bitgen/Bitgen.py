import BitcoinUtils
import FileUtils


class BitGen:
    def __init__(self, bitcoinWalLoc, walletBackLoc, keyFilesLoc):
        self.bitcoind = BitcoinUtils.BUtils()
        self.fileUtils = FileUtils.FUtils(bitcoinWalLoc, walletBackLoc, keyFilesLoc)
        self.keyFiles = self.fileUtils.keyFiles()
        self.run()

    def run(self):
        if self.bitcoind.isRunning():
            self.bitcoind.stop()
        self.bitcoind.start()


if __name__ == '__main__':
    BitGen("/home/zebub/.bitcoin/", "/home/zebub/walletBackup/", "/home/zebub/code/keysRepo")
