import glob
import os


class FUtils:
    def __init__(self, bitcoinWalLoc, walletBackLoc, keyFilesLoc):
        self.bitcoinWallet = "{}wallet.dat".format(bitcoinWalLoc)
        self.walletBackupLoc = walletBackLoc
        self.keyFilesDir = keyFilesLoc

    def keyFiles(self):
        return sorted(glob.glob("{}*.txt".format(self.keyFilesDir)))

    def keyList(self, path):
        with open(path) as f:
            content = f.readlines()
        return [x.strip() for x in content]

    def backupWallet(self, backupName="unknown"):
        backupWallet = "{}wallet.dat.{}".format(self.walletBackupLoc, backupName)
        os.rename(self.bitcoinWallet, backupName)