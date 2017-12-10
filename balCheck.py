import requests
import json
import sys
import os
import random
from time import sleep

watchList = []
goldList = []
isLinux = sys.platform.lower().startswith('linux')

def getAccts(url):



def checkBalance(acctData):
    sleep(2)
    url1 = "https://blockchain.info/balance?active={}".format(acctData[1].strip())
    url2 = "https://blockchain.info/balance?active={}".format(acctData[2].strip())
    r1 = requests.get(url1)
    r2 = requests.get(url2)
    final1 = 0
    final2 = 0
    tot1 = 0
    tot2 = 0

    if r1.status_code is not 200 or r2.status_code is not 200:
        print("cant look up bal, blockchain api issue")

    if r1.status_code == 200:
        acctCheck1 = json.loads(r1.content.decode('utf-8'))[acctData[1].strip()]
        final1 = acctCheck1['final_balance']
        tot1 = acctCheck1['total_received']

    if r2.status_code == 200:
        acctCheck2 = json.loads(r2.content.decode('utf-8'))[acctData[2].strip()]
        final2 = acctCheck2['final_balance']
        tot2 = acctCheck2['total_received']

    if final1 > 0 or final2 > 0:
        print()
        print("*!*"*100)
        print("GOT ONE!!!!!!!!!!!!!!!1")
        print(acctData)
        print("{} {} {} {} -- {}".format(final1, final2, tot1, tot2, numbOfAccounts))
        print("*!*"*100)
        print()
        goldList.append(acctData)

    if tot1 > 0 or tot2 > 0:
        print()
        print("*"*50)
        print("WATCH OUT!!!!!")
        print(acctData)
        print("{} {} {} {} -- {}".format(final1, final2, tot1, tot2, numbOfAccounts))
        print("*"*50)
        print()
        watchList.append(acctData)


workDir = '/var/www/html/bitcon' if isLinux else 'C:\\bitcon'

if not os.path.exists(workDir):
    os.makedirs(workDir)
    seed = random.getrandbits(128)

    if len(goldList) > 0:
        with open("{}{}.gold.txt".format(workDir, seed), "w") as f:
            for gold in goldList:
                f.write("{}, {}, {}\n".format(gold[0], gold[1], gold[2]))
        goldList = []

    if len(watchList) > 0:
        with open("{}{}.watch.txt".format(workDir, seed), "w") as f:
            for watch in watchList:
                f.write("{}, {}, {}\n".format(watch[0], watch[1], watch[2]))
        watchList = []
else:
    print("Nothing to do! Exiting...")
    exit()
