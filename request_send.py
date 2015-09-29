import urllib2
import sys
import threading
import random
import re
import logging
import json

url = ''
param = ''
header = {}
cookies = ''
local = threading.local()
request_counter = 1
thread_counter = 1
run_counter = 1
success = 0 
fail = 0
lock = threading.Lock()
logger = logging.getLogger('mylogger')


def inc_counter():
    global run_counter
    run_counter+=1

def httpcall():
    code = 0
    global param
    global header
    try:
      cookieHandle = urllib2.HTTPCookieProcessor()
      opener = urllib2.build_opener(cookieHandle)
      # opener = addHeader(opener)
      opener = addCookie(opener)
      urllib2.install_opener(opener)
      if len(param)>0:
          # param = json.dumps(param)
          request = urllib2.Request(url,param,header)
      else:
          request = urllib2.Request(url)
      response = opener.open(request)
      body = response.read()
      print "body:%s"%body
      logger.info(body)
    except urllib2.HTTPError, e:
      local.fail+=1
      print 'Response Code 500'
      code=500
    except urllib2.URLError, e:
      print e.reason
      sys.exit()
    else:
      local.success+=1
      # local.data.append(body)
    return(code)

def addHeader(opener):
    global header
    if len(header)>0:
          for (key,value) in header.items():
            opener.addheaders.append(key,value)
    return opener

def addCookie(opener):
    global cookies
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
    # if len(sys.argv) < 3:
    #   sys.exit()
    # else:
      # url = sys.argv[2]
      # if len(sys.argv)== 3:
      #     thread_counter = sys.argv[3]
      # if len(sys.argv)==4:
      #     request_counter = sys.argv[4]
      # if len(sys.argv)==5:
      #     param = sys.argv[5]
      # if len(sys.argv)==6:
      #     header = sys.argv[6]
      # if len(sys.argv)==7:
      #     cookies = sys.argv[7]
    #url = "http://baichuan.baidu.com/rs/adp/launch?placeId=1427086959682&callback=bc6815431443148898986&referUrl=&curUrl=http%3A%2F%2Fvideo.baidu.com%2F&v=2.0.5&guid=9d8db513-c91a-4aca-a1bd-3abbab3925a7"
    url = "http://cp01-testing-dianquan06.cp01.baidu.com:8282/ebgmt-jersey-estimate-web/estimate/queryEstimate"
    param = '{"userIDType": "USERID", "businessID": 1, "userID": 1109283250, "tag": 13, "estimateAdsList": [{"estimateAdsID": 16997, "estimateAdsInfoForTB": {"province": "", "uid": 1109283250, "obj_subtype": "\u4f1a\u5458", "obj_good_id": 29548, "cuid": "", "t_provid": "", "obj_type": "\u7528\u6237\u6d88\u8d39", "clicked": 0, "obj_throw_type": "BY_FORUM", "bdid": "ABB2EC2708CFF656B857A04F833FD2DB", "fid": 194961, "obj_cpid": 5, "obj_plan": 1, "locate": "p0005", "fname": "", "obj_spec": "", "tid": 0, "second_dir": "\u5e7f\u4e1c\u9662\u6821", "idfa": "", "imei": "", "refer": "http://tieba.baidu.com/f?kw=%C9%EE%DB%DA%D6%B0%D2%B5%BC%BC%CA%F5%D1%A7%D4%BA&fr=ala0&tpl=5", "first_dir": "\u9ad8\u7b49\u9662\u6821", "obj_ref": "", "obj_loc_param": "", "obj_id": 16997, "url": "/billboard/pushlog/?t=1441701871872&r=1112494348548352&client_type=pc_web&task=tbda&page=frs&fid=194961&tid=&uid=1109283250&da_task=tbda&da_fid=194961&da_tid=&da_uid=1109283250&da_page=frs&da_type_id=0001&da_obj_id=16997&da_good_id=29548&da_obj_name=%E7%99%BE%E5%BA%A6VIP%E5%90%88%E4%BD%9C%E6%B4%BB%E5%8A%A8&da_first_name=%E7%94%A8%E6%88%B7%E6%B6%88%E8%B4%B9&da_second_name=%E4%BC%9A%E5%91%98&da_cpid=5&da_abtest=&da_price=100&da_verify=84c758532855026d6708577c48cbb7fc&da_plan_id=1&da_ext_info=1_0_0_0_5_0_0_0_p0005_%E9%AB%98%E7%AD%89%E9%99%A2%E6%A0%A1_%E5%B9%BF%E4%B8%9C%E9%99%A2%E6%A0%A1_%E7%99%BE%E5%BA%A6VIP%E5%90%88%E4%BD%9C%E6%B4%BB%E5%8A%A8_%E7%94%A8%E6%88%B7%E6%B6%88%E8%B4%B9_%E4%BC%9A%E5%91%98_f2b7dd3ee380a978427b1d469bddbe8a&da_client_type=PC&da_throw_type=0&da_loc_index=1&locate=25&da_locate=25&type=show&da_type=show", "obj_price": 100.0, "obj_vdir": "", "obj_form": "", "client_type": "pc_web", "net_type": "", "obj_charge_type": "", "obj_uid": 1109283250, "os": "", "page": "FRS"}}], "estimateID": "TB13"}'
    header = {'Content-Type':'text/plain;charset=utf-8'}
    thread_counter = 5
    request_counter = 5

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
    
        if run_counter == total_counter:
           print "\n-- HULK Attack Finished --"
           print("success:%s"%success)
           print("fail:%s"%fail)
           break


class HTTPThread(threading.Thread):
    def run(self):
      count = 0
      global success
      global fail
      local.success = 0
      local.fail = 0
      global request_counter
      try:
        # print("flag:%d count:%d thread_counter:%d"%(flag,count,request_counter))
        while count<request_counter:
            code = httpcall()
            count +=1
        if lock.acquire():
           success = success + local.success
           fail = fail + local.fail
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
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)

if __name__ == '__main__':
  main()



