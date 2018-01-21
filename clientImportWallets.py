import glob
from subprocess import Popen, PIPE

importCount = 0


def getWalletFiles(direct):
    walletFiles = glob.glob("{}/*.txt".format(direct))
    for walFile in walletFiles:
        readWalletFile(walFile)


def readWalletFile(fname):
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    for wal in content:
        runCommand(wal, fname)


def runCommand(priKey, fname):
    global importCount
    importCount += 1
    fname = fname.split('/')[len(fname.split('/')) - 1].replace(".txt", '')
    cmd = "bitcoin-cli importprivkey {} \"{}\" false".format(priKey, fname)
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print
    print "{} - {} --Count: {}".format(priKey, fname, importCount)
    print out
    print err
    print "-" * 50


getWalletFiles('/home/zebub/code/keyfiles2')