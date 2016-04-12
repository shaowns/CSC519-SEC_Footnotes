#!/usr/bin/python

import MySQLdb
import os
import sys

db = MySQLdb.connect("localhost", "team4", "team4", "sec")
cursor = db.cursor()
companies_query = "SELECT * FROM companies"
cursor.execute(companies_query)
data = cursor.fetchall()
for row in data:   
	print "c_id : %s\t c_name: %s" % (row[0], row[1])
	for i in range(1993,2017):
		for quarter in range(1,5):
			query = "python sec_ftp_fetch.py %s %s %s" % (row[1], i, quarter)
			os.system(query)
cursor.close()

db.close()
sys.exit()
