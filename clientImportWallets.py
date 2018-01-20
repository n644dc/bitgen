import glob
from subprocess import Popen, PIPE


def getWalletFiles(direct):
    walletFiles = glob.glob("{}/*.txt".format(direct))
    for walFile in walletFiles:
        readWalletFile(walFile)


def readWalletFile(fname):
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    for wal in content:
        runCommand(wal)


def runCommand(priKey):
    cmd = "bitcoin-cli importprivkey {} \"fart1\" false".format(priKey)
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print
    print out
    print err
    print "-" * 50


getWalletFiles('/bitcon')
