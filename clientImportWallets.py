import glob
import json
from subprocess import Popen, PIPE


jsonWalletArray = []


def importCLI():
    cmd = "bitcoin-cli importmulti '{}'".format(jsonWalletArray)
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()


def getWalletFiles(direct):
    walletFiles = glob.glob("{}\\*.txt".format(direct))

    # Put into and array of json objects
    for walFile in walletFiles:
        readWalletFile(walFile)

    importCLI()


def readWalletFile(fname):
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    for wal in content:
        walArr = wal.split(',')
        pubKey = walArr[5].strip()
        label = "topMillion"
        scriptPubKey = {}
        jWal = {}
        scriptPubKey["address"] = pubKey
        jWal["scriptPubKey"] = scriptPubKey
        jWal["timestamp"] = "0"
        jWal["label"] = label
        jsonWallet = json.dumps(jWal)
        jsonWalletArray.append(jsonWallet)


getWalletFiles('C:\\bitcon\\watches_700500')
