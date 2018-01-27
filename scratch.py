import glob
from subprocess import Popen, PIPE

fileCount = 0
importCount = 0
walName = 'test'


def getWalletFiles(direct):
    global fileCount
    walletFiles = glob.glob("{}/*.txt".format(direct))
    for walFile in sorted(walletFiles):
        fileCount += 1
        if fileCount < 11:
            readWalletFile(walFile)
        else:
            exit()


def readWalletFile(fname):
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    for wal in content:
        runCommand(wal)


def runCommand(priKey):
    global importCount
    global walName
    importCount += 1

    if importCount % 50 == 0:
        walName = "test_" + str(importCount)

    cmd = "bitcoin-cli importprivkey {} \"{}\" false".format(priKey, walName)
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print
    print "{} - {} --Count: {}".format(priKey, walName, importCount)
    print out
    print err
    print "-" * 50


getWalletFiles('/home/zebub/32mill')
