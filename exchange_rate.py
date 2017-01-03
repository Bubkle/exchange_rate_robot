# -*- coding:utf-8 -*-

import urllib2
import json
from urllib import urlencode
from pymongo import MongoClient
import datetime
import sys
from send_email import email
import time

reload(sys)
sys.setdefaultencoding('utf-8')

client = MongoClient('localhost', 27017)
db = client.exchange_rate
appkey = '10003'
sign = 'b59bc3ef6191eb9f747dd4e83c99f2a4'
url = 'http://api.k780.com:88'
data = {
	 'app' : 'finance.rate_cnyquot',
 	 'curno' : 'GBP',
	 'appkey' : appkey,
	 'sign' : sign,
	 'format' : 'json',	
}

data = urlencode(data)
url = url + '?' + data
while True:
	response = urllib2.urlopen(url)
	result = response.read()

	if result:
		result = json.loads(result)
		GBP = db.GBP
		lowest = ''
		if result['success']=='1':
			bankno = ['BOC', 'CCB', 'ICBC', 'ABC', 'CEB']
			for item in result['result'].values(): 
				for no in bankno:
					if item.has_key(no):
						data = {}
						upddate = item[no]['upddate']
						data['banknm'] = item[no]['banknm']
						data['upddate'] = datetime.datetime.strptime(upddate, '%Y-%m-%d %H:%M:%S')
						data['rate'] = float(item[no]['cn_buy']) / 100
						data['tuition'] = data['rate'] * 21500
						GBP.insert_one(data)
						docs = GBP.find({"rate": {"$lt": data['rate']}})
						if docs.count() == 0:
							lowest = "历史最低汇率%s，来自%s，tuition为%s" % (str(data['rate']), str(data['banknm']), str(data['tuition']))
			if lowest:
				print email(lowest)
		else:
			print 'failed'
	else:
		print 'no result'

	time.sleep(3600)	
