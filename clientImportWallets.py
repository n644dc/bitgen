import glob
import json
from time import sleep
from subprocess import Popen, PIPE

jsonWalletArray = []



def importCLI():
    segmentArray = []
    count = 0
    for wallet in jsonWalletArray[99:]:
        segmentArray.append(wallet)
        count += 1
        if count % 100 == 0:
            runCommand(json.dumps(segmentArray))
            segmentArray = []


def runCommand(segmentArray):
        cmd = "bitcoin-cli importprivkey '{}' \"{}\" false".format(segmentArray, "aWalletName")
        cmd += " '{ \"rescan\": true }'"
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
        jWal["timestamp"] = 0
        jWal["label"] = label
        jsonWalletArray.append(jWal)


getWalletFiles('C:\\bitcon\\watches_700500')
