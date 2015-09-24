import urllib2
import sys
import threading
import random
import re

url = ''
param = ''
header = {}
cookies = ''
local = threading.local()
request_counter = 1
total_counter = 0
thread_counter = 0
lock = threading.Lock()


def inc_counter():
    global request_counter
    request_counter+=1

def httpcall():
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
    except urllib2.HTTPError, e:
      #print e.code
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
    if len(sys.argv) < 3:
      sys.exit()
    else:
      url = sys.argv[2]
      if len(sys.argv)== 3:
          param = sys.argv[3]
      if len(sys.argv)==4:
          header = sys.argv[4]
      if len(sys.argv)==5:
          cookies = sys.argv[5]
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
      while flag==0 :
        # print("request_counter:%d total_counter:%d"%(request_counter,total_counter))
        if (previous+100<request_counter) and (previous!=request_counter):
           print("%d Requests Sent"%request_counter)
           previous=request_counter
        #批量把global中的data进行转移，并且进行log
        if request_counter == total_counter:
           print "\n-- HULK Attack Finished --"
           print("success:%s"%success)
           print("fail:%s"%fail)
           break


class HTTPThread(threading.Thread):
    def run(self):
      try:
        count = 0
        # print("flag:%d count:%d thread_counter:%d"%(flag,count,thread_counter))
        while count<thread_counter:
          # print"test"
            code = httpcall()
            if count<100: 
              if lock.acquire():
                  #把local.data的值复制给global的data
                
        if lock.acquire():
           #线程结束，统计成功失败

          # if (code==500) :
          #   set_flag(2)
      except Exception, e:
        raise

def main():
  global thread_counter
  global total_counter
  thread_counter = 10
  total_counter = 100
  for i in range(10):
      t = HTTPThread()
      t.start()
  t = MonitorThread()
  t.start()

if __name__ == '__main__':
  main()



