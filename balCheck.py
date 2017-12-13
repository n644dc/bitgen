import requests
import json
import sys
import os
import random
import logging
import datetime
from subprocess import Popen, PIPE
from time import sleep

watchList = []
goldList = []
startingPlace = 38761
isLinux = sys.platform.lower().startswith('linux')
workDir = '/var/www/html/bitcon' if isLinux else 'C:\\bitcon'
logfile = "{}/loggo.txt".format(workDir) if isLinux else "{}\\loggo.txt"

if not os.path.exists(workDir):
    os.makedirs(workDir)

logging.basicConfig(filename=logfile, level=logging.INFO)

goldDir = "{}/{}".format(workDir, 'gold') if isLinux else "{}\\{}\\".format(workDir, 'gold')
watchDir = "{}/{}/".format(workDir, 'watch') if isLinux else "{}\\{}\\".format(workDir, 'watch')

if not os.path.exists(goldDir):
    os.makedirs(goldDir)

if not os.path.exists(watchDir):
    os.makedirs(watchDir)


def saveWallet(wallet, typeu):
    seed = random.getrandbits(64)
    if typeu == 'gold':
        savFile = "{}{}.gold.txt".format(goldDir, seed)
    else:
        savFile = "{}{}.watch.txt".format(watchDir, seed)

    with open(savFile, "w") as f:
        f.write(", ".join(wallet))
    logging.info("{} wallet saved".format(datetime.datetime.now()))


def getAccts(url):
    req = requests.get(url)
    if req.status_code is not 200:
        print("Get Accounts page: ip changed or not reachable")
    else:
        content = req.content.decode('utf-8')
        content = content.split(',')
        content = [x.strip() for x in content]
        logging.info("{} Checking Accounts for: {}".format(datetime.datetime.now(), url))
        for page in content:
            getWallets(page)


def isRepeat(pubKey, id_str):
    cmd = "grep -nr {} {}".format(pubKey, workDir)
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    wid = int(id_str)
    if wid < startingPlace:
        logging.info("{} Repeat: {} #: {}".format(datetime.datetime.now(), pubKey, id_str))
        return False

    if len(out.strip()) > 10:
        logging.info("{} Repeat: {} #: {}".format(datetime.datetime.now(), pubKey, id_str))
        return True
    else:
        return False


def getWallets(page):
    req = requests.get(page)
    if req.status_code is not 200:
        msg = "Get Wallet Txt file: not reachable"
        logging.info(msg)
        print(msg)
    else:
        logging.info("{} Getting Wallets from Page: {}".format(datetime.datetime.now(), page))
        content = req.content.decode('utf-8')
        content = [s.strip() for s in content.splitlines()]
        for walletRaw in content:
            wallet = walletRaw.split(',')
            wallet = [x.strip() for x in wallet]
            if not isRepeat(wallet[5].strip(), wallet[0].strip()):
                checkBalance(wallet)


def checkBalance(wallet):
    sleep(2)
    url1 = "https://blockchain.info/balance?active={}".format(wallet[5].strip())
    r1 = requests.get(url1)
    final1 = 0
    tot1 = 0

    if r1.status_code is not 200:
        msg = "cant look up bal, blockchain api issue"
        logging.info(msg)
        print(msg)

    if r1.status_code == 200:
        acctCheck1 = json.loads(r1.content.decode('utf-8'))[wallet[5].strip()]
        final1 = acctCheck1['final_balance']
        tot1 = acctCheck1['total_received']

    if final1 > 0:
        logging.info("GOLD FOUND")
        print
        print("*!*" * 100)
        print("GOT ONE!!!!!!!!!!!!!!!1")
        print(wallet)
        print("{} {}".format(final1, tot1))
        print("*!*" * 100)
        print
        saveWallet(wallet, 'gold')

    if tot1 > 0:
        logging.info("Active Wallet Found")
        print
        print("*" * 50)
        print("WATCH OUT!!!!!")
        print(wallet)
        print("{} {}".format(final1, tot1))
        print("*" * 50)
        print
        saveWallet(wallet, 'watch')


getAccts('http://172.26.14.114/acct_files.php')
