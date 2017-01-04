# -*- coding:utf-8 -*-
from pymongo import MongoClient
from bson.son import SON
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

client = MongoClient('localhost', 27017)
db = client.exchange_rate
GBP = db.GBP
pipeline = [
	{"$group": {"_id": "$banknm", "avg_rate": {"$avg": "$rate"}, "avg_tuition": {"$avg": "$tuition"}}},
	{"$sort": SON([("avg_tuition", 1)])},
]
result = GBP.aggregate(pipeline)
if result:
	for item in result:
		print "银行名称：%s, 平均汇率：%s, 平均tuition：%s\n" %(item['_id'], item['avg_rate'], item['avg_tuition'])

else:
	print "no result"
