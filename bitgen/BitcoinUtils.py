from subprocess import Popen, PIPE
import logging
import datetime


class BUtils:
    def __init__(self):
        self.STOPPING = 'stopping'
        self.STARTING = 'starting'
        self.STOPPED = 'stopped'
        self.RUNNING = 'running'
        self.STATE = 'stopped'
        logfile = '/home/zebub/bitgenLogs/bitUtilsLog.txt'
        logging.basicConfig(filename=logfile, level=logging.INFO)
        logging.info("{} Bitgen Started".format(datetime.datetime.now()))

    @staticmethod
    def runCommand(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()

        return out, err

    def start(self, isRescan = False):
        cmd = "bitcoind -daemon -server=1"
        if isRescan:
            cmd += " -rescan"
        out, err = self.runCommand(cmd)
        logging.info("{} ran command: {} -_-_-_- out: {}  -+-+- err: {}".format(datetime.datetime.now(), cmd, out, err))
        if len(out) < 1:
            self.STATE = self.STARTING
            self.waitTillRunning()
            return True
        return False

    def stop(self):
        cmd = "bitcoin-cli stop"
        out, err = self.runCommand(cmd)
        logging.info("{} ran command: {} -_-_-_- out: {}  -+-+- err: {}".format(datetime.datetime.now(), cmd, out, err))
        if self.STOPPING in out:
            self.STATE = self.STOPPING
            self.waitTillStopped()
            return True
        return False

    def isRunning(self):
        if '"":' in self.listAccounts():
            return True
        return False

    def waitTillRunning(self):
        loop = True
        while loop:
            if self.isRunning():
                loop = False

    def waitTillStopped(self):
        loop = True
        while loop:
            if not self.isRunning():
                loop = False

    def listAccounts(self):
        cmd = "bitcoin-cli listaccounts"
        out, err = self.runCommand(cmd)
        return out

    def importKey(self, priKey, walletName):
        cmd = "bitcoin-cli importprivkey {} \"{}\" false".format(priKey, walletName)
        out, err = self.runCommand(cmd)
        if len(err.strip()) < 5:
            return True
        else:
            return False
