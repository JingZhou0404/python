# -*- coding: utf-8 -*-
import xlrd
import xlwt
import urllib
import urllib2
from xlutils.copy import copy
import json
import sys
import re


reload(sys)
sys.setdefaultencoding('utf8')
businessID = 1
estimateModelID=0
# url = "http://nj02-dianquan00.nj02.baidu.com:8182/ebgmt-jersey-estimate-web/estimate/queryEstimate";
url = "http://cp01-testing-dianquan06.cp01.baidu.com:8282/ebgmt-jersey-estimate-web/estimate/queryEstimate"

def open_excel():
    #book  = xlrd.open_workbook("C:\\Users\\zhoujing08\\Desktop\\模型测试列表.xlsx")
    book  = xlrd.open_workbook("test.xls")
    table = book.sheet_by_index(0)
    newbook = copy(book)
    newtable = newbook.get_sheet(0)
    return table,newtable,newbook

def http_post(url,value):
    headers = {
    'Content-Type': 'text/plain; charset=utf-8',
    'Content-Length': len(value),
    }
    req = urllib2.Request(url, value,headers)
    response = urllib2.urlopen(req)
    return response.read()

def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]

def juge(value):
    value = str(value)
    if value=='':
        return ''
    elif re.match(r"[0-9]*[.][0-9]+$", value) :
        return int(float(value))
    else:
        print value
        return value
def bidOrcuid(value1,value2):
    userIDType = 'BAIDUID'
    if value1=='':
        userIDType = 'CUID'
        return value2,userIDType
    return value1,userIDType

def set_bdid(value):
    if value != '':
       value = value.split(':')[0]
    return value

def main():
    col_value = 0
    modele_1 = 0
    modele_2 = 0
    modele_0 = 0
    table,newtable,newbook=open_excel()
    for rx in range(1,table.nrows):
        tag = rx + 10
        estimateID = "TB" + str(tag)
        userID = juge(table.cell_value(rowx=rx,colx=22))
        baiduUserID = set_bdid(table.cell_value(rowx=rx,colx=18))
        clientUserID = table.cell_value(rowx=rx,colx=20)
        estimateAdsID = juge(table.cell_value(rowx=rx,colx=4))
        estimateAdsInfo = {}
        estimateAdsInfo['page'] = table.cell_value(rowx=rx,colx=0)
        estimateAdsInfo['locate'] = table.cell_value(rowx=rx,colx=1)
        estimateAdsInfo['obj_loc_param'] = table.cell_value(rowx=rx,colx=2)
        estimateAdsInfo['obj_plan'] = juge(table.cell_value(rowx=rx,colx=3))
        estimateAdsInfo['obj_id'] = juge(table.cell_value(rowx=rx,colx=4))
        estimateAdsInfo['obj_type'] = table.cell_value(rowx=rx,colx=5)
        estimateAdsInfo['obj_subtype'] = table.cell_value(rowx=rx,colx=6)
        estimateAdsInfo['obj_cpid'] = juge(table.cell_value(rowx=rx,colx=7))
        estimateAdsInfo['obj_form'] = table.cell_value(rowx=rx,colx=8)
        estimateAdsInfo['obj_good_id'] =juge(table.cell_value(rowx=rx,colx=9))
        estimateAdsInfo['obj_spec'] = table.cell_value(rowx=rx,colx=10)
        estimateAdsInfo['obj_price'] = table.cell_value(rowx=rx,colx=11)
        estimateAdsInfo['obj_vdir'] = table.cell_value(rowx=rx,colx=12)
        estimateAdsInfo['obj_ref'] = table.cell_value(rowx=rx,colx=13)
        estimateAdsInfo['obj_uid'] = juge(table.cell_value(rowx=rx,colx=14))
        estimateAdsInfo['obj_throw_type'] = table.cell_value(rowx=rx,colx=15)
        estimateAdsInfo['obj_charge_type'] = table.cell_value(rowx=rx,colx=16)
        estimateAdsInfo['client_type'] = table.cell_value(rowx=rx,colx=17)
        estimateAdsInfo['bdid'] = set_bdid(table.cell_value(rowx=rx,colx=18))
        estimateAdsInfo['imei'] = table.cell_value(rowx=rx,colx=19)
        estimateAdsInfo['cuid'] = table.cell_value(rowx=rx,colx=20)
        estimateAdsInfo['idfa'] = table.cell_value(rowx=rx,colx=21)
        estimateAdsInfo['uid'] = juge(table.cell_value(rowx=rx,colx=22))
        estimateAdsInfo['fid'] = juge(table.cell_value(rowx=rx,colx=23))
        estimateAdsInfo['fname'] = table.cell_value(rowx=rx,colx=24)
        estimateAdsInfo['first_dir'] = table.cell_value(rowx=rx,colx=25)
        estimateAdsInfo['second_dir'] = table.cell_value(rowx=rx,colx=26)
        estimateAdsInfo['tid'] = juge(table.cell_value(rowx=rx,colx=27))
        estimateAdsInfo['t_provid'] = table.cell_value(rowx=rx,colx=28)
        estimateAdsInfo['os'] = table.cell_value(rowx=rx,colx=29)
        estimateAdsInfo['net_type'] = table.cell_value(rowx=rx,colx=30)
        estimateAdsInfo['url'] = table.cell_value(rowx=rx,colx=31)
        estimateAdsInfo['refer'] = table.cell_value(rowx=rx,colx=32)
        estimateAdsInfo['clicked'] = juge(table.cell_value(rowx=rx,colx=33))
        #estimateAdsInfo['clicked'] = table.cell_value(rowx=rx,colx=33)
        estimateAdsInfo['province'] =""

        estimateAdsList = []
        estimateAdsList.append({"estimateAdsID":estimateAdsID,"estimateAdsInfoForTB":estimateAdsInfo})

        data = {}
        data['tag'] = tag
        data['estimateID'] = estimateID
        data['businessID'] = businessID
        #data['estimateModelID'] = estimateModelID
        data['estimateAdsList'] = estimateAdsList
        if rx<=1000:
            data['userID'] = userID
            data['userIDType'] = 'USERID'
        else:
            data['userID'],data['userIDType'] = bidOrcuid(baiduUserID,clientUserID)
        #data['baiduUserID'] = baiduUserID
        #data['clientUserID'] = clientUserID
        data_string = json.dumps(data)

        newtable.write(rx,34,data_string)
        try:
            # print userID
            if (userID!="0"):
                resp = http_post(url,data_string)
                decodejson = json.loads(resp)
        except Exception, e:
            raise e

        print("line:%d result:%s"%(rx,resp))
        newtable.write(rx,35,resp)
        if len(decodejson["estimateAdsResultList"])!=0:
            newtable.write(rx,36,decodejson["estimateAdsResultList"][0]["estimateAdsWeight"])
            newtable.write(rx,37,decodejson["estimateModelID"])
            if float(decodejson["estimateAdsResultList"][0]["estimateAdsWeight"])<0:
                col_value = col_value + 1
            if str(decodejson["estimateModelID"]) == "1":
                modele_1 = modele_1 + 1
            elif str(decodejson["estimateModelID"])=="2":
                modele_2 = modele_2 + 1
            elif str(decodejson["estimateModelID"])=="0":
                modele_0 = modele_0 + 1
            else :
                pass
    newbook.save("test.xls")
    print ("col_value:%d"%col_value)
    print("modele_1:%s modele_2:%s modele_0:%s"%(modele_1,modele_2,modele_0))
    print "save file ok"

if __name__ =="__main__":
    main()







