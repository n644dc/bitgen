import requests
import json
import sys
import os
import random
from subprocess import Popen, PIPE
from time import sleep

watchList = []
goldList = []
isLinux = sys.platform.lower().startswith('linux')
workDir = '/var/www/html/bitcon' if isLinux else 'C:\\bitcon'

if not os.path.exists(workDir):
    os.makedirs(workDir)

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


def getAccts(url):
    req = requests.get(url)
    if req.status_code is not 200:
        print("Get Accounts page: ip changed or not reachable")
    else:
        content = req.content.decode('utf-8')
        content = content.split(',')
        content = [x.strip() for x in content]

        for page in content:
            getWallets(page)


def isRepeat(pubKey):
    cmd = "grep -nr '{}' {}".format(pubKey, workDir)
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print "Return code: ", p.returncode
    print out.rstrip(), err.rstrip()
    if len(out.strip()) < 1:
        return False
    else:
        return True


def getWallets(page):
    req = requests.get(page)
    if req.status_code is not 200:
        print("Get Wallet Txt file: not reachable")
    else:
        content = req.content.decode('utf-8')
        content = [s.strip() for s in content.splitlines()]
        for walletRaw in content:
            wallet = walletRaw.split(',')
            wallet = [x.strip() for x in wallet]

            if not isRepeat(wallet[5].strip()):
                checkBalance(wallet)


def checkBalance(wallet):
    sleep(2)
    url1 = "https://blockchain.info/balance?active={}".format(wallet[5].strip())
    r1 = requests.get(url1)
    final1 = 0
    tot1 = 0

    if r1.status_code is not 200:
        print("cant look up bal, blockchain api issue")

    if r1.status_code == 200:
        acctCheck1 = json.loads(r1.content.decode('utf-8'))[wallet[5].strip()]
        final1 = acctCheck1['final_balance']
        tot1 = acctCheck1['total_received']

    if final1 > 0:
        print
        print("*!*" * 100)
        print("GOT ONE!!!!!!!!!!!!!!!1")
        print(wallet)
        print("{} {}".format(final1, tot1))
        print("*!*" * 100)
        print
        saveWallet(wallet, 'gold')

    if tot1 > 0:
        print
        print("*" * 50)
        print("WATCH OUT!!!!!")
        print(wallet)
        print("{} {}".format(final1, tot1))
        print("*" * 50)
        print
        saveWallet(wallet, 'watch')


getAccts('http://18.217.247.116/acct_files.php')
