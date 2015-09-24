from time import sleep
from random import random
from threading import Thread, local
import threading
import logging 
data = local()
lock = threading.Lock()
total = 0
response = []
logger = logging.getLogger('mylogger')

 
def bar():
    print 'called from %s'%data.v
 
def foo():
    data.v = str(data.v) + '.......'
    bar()
def count():
    data.count +=1
    data.response.append("test")
 
class T(Thread):
    def run(self):
        data.count = 0
        data.response = []
        global logger
        # print data.count
        while data.count<10:
            count()
            logger.info("%s--count%d "%(str(self.getName()),data.count))
            print("%s--count%d "%(str(self.getName()),data.count))
        if lock.acquire():
            global total
            global response
            total = total + data.count
            response.append(data.response)
            print "total:",total
            print "response:",len(response)
            lock.release()
        

def main():
    global logger
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    for x in xrange(1,10):
        t = T()
        t.start()
if __name__ == '__main__':
    main()
