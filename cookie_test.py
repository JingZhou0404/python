import httplib2
import urllib
import urllib2
import cookielib

def main():
    cookies = 'BAIDUID=33A8751EC413263F55A194607E9F35C7:FG=1;BDUSS=UQ3QX54bWFOWkxUcVRkckl2TXFlUFU3ZWVsWFlMSnI2T2RnMWZkMW8zLUVzaUZXQVFBQUFBJCQAAAAAAAAAAAEAAAAxhABzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIQl;'
    conn = httplib.HTTPSConnection("www.baidu.com")
    conn.request("GET","/",headers={'Cookie':cookies})
    res = conn.getresponse()
    print "cookies result :",res.read()
    print "-============"
    conn.close()
    conn = httplib.HTTPSConnection("www.baidu.com")
    conn.request("GET","/")
    res = conn.getresponse()
    print "no cookies result :",res.read()
    conn.close()

def main1():
    url ="http://baichuan.baidu.com/rs/adp/launch?placeId=1427086959682&callback=bc1163501442919206760&referUrl=&curUrl=http%3A%2F%2Fvideo.baidu.com%2F&v=2.0.5&guid=047133c7-0017-4b4c-8c33-215280b6d11e"
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    print response.read()
def main2():
    url ="http://baichuan.baidu.com/rs/adp/launch?placeId=1427086959682&callback=bc1163501442919206760&referUrl=&curUrl=http%3A%2F%2Fvideo.baidu.com%2F&v=2.0.5&guid=047133c7-0017-4b4c-8c33-215280b6d11e"
    http=httplib2.Http()
    response, content = http.request(url, 'GET')
    print content
def main3():
    loginUrl = "http://passport.baidu.com";
    cj = cookielib.CookieJar();
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
    urllib2.install_opener(opener);
    resp = urllib2.urlopen(loginUrl);
    for index, cookie in enumerate(cj):
        print '[',index, ']',cookie;
if __name__ == '__main__':
  main3()
