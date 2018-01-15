import glob
import json
from time import sleep
from subprocess import Popen, PIPE

jsonWalletArray = []


def runCommand(priKey, label):
    cmd = "bitcoin-cli importprivkey {} \"{}\" true".format(priKey, label)
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print
    print
    print out
    print err
    print
    print
    sleep(1)


def getWalletFiles(direct):
    walletFiles = glob.glob("{}\\*.txt".format(direct))

    # Put into and array of json objects
    for walFile in walletFiles:
        readWalletFile(walFile)


def readWalletFile(fname):
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    for wal in content:
        walArr = wal.split(',')
        priKey = walArr[3].strip()
        label = "topMillion"
        runCommand(priKey, label)


getWalletFiles('C:\\bitcon\\watches_700500')
