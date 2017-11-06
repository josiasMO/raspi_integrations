#!/usr/bin/env python
# *-* coding: utf-8 *-*

import subprocess
import threading
import socket
import os, sys
import time
import logging


class Encoding(object):
    def __init__(self):
        pass


class GPRS(object):
    def __init__(self, host='rasp.dalmago.xyz', port=5555):
        self.status = None
        self.proc = None
        self.host = host
        self.port = port

    def __ppp0status(self):
        """Check if the ppp0 connection is ready"""
        try:
            f = open("/sys/class/net/ppp0/operstate","r")
            if (f.readline() == 'unknown\n'):
                print('[PPPD]: ppp0 interface is UP')
                return 1
        except:
            return 0

    def __conn(self, data):
        """Open tcp socket and send data to the specified host"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(15)
        recv = None
        try:
            s.connect((self.host, self.port))
            s.sendall(data.encode(encoding='utf-8'))
            recv = s.recv(1024)
        except socket.error as msg:
            recv = None
            print ("Type Error: %s" % msg)
        finally:
            s.close()
            return recv

    def __procout(self, proc):
        """handle pppd subprocess output"""
        for line in iter(proc.stdout.readline, b''):
            print('[PPPD]: {0}'.format(line.decode('utf-8')), end='')

    def send(self,data):
        """start pppd subprocess, """
        proc = subprocess.Popen(['pppd','call','gprs'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)

        t = threading.Thread(target=self.__procout, args=(proc,))
        t.start()

        try:
            while proc.poll() is None:
                if(self.__ppp0status()):
                    #encoding data here
                    d = self.__conn (data)
                    if d is not None:
                        proc.terminate()
                time.sleep(0.5)
        finally:
            print('[PPPD]: Terminate pppd process')
            proc.terminate()
            try:
                proc.wait(timeout=2)
                print('== subprocess exited with rc =', proc.returncode)
            except subprocess.TimeoutExpired:
                print('subprocess did not terminate in time')
        t.join()


if __name__ == "__main__":
    g = GPRS()
    g.send('123')
