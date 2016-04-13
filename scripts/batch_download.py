#!/usr/bin/python
#default values for year: 1993, 2017
#default values for quarter: 1, 5

import os
import sys
#import MySQLdb

#db = MySQLdb.connect("localhost", "team4", "team4", "sec")
#cursor = db.cursor()
#companies_query = "SELECT * FROM companies"
#cursor.execute(companies_query)
#data = cursor.fetchall()
data = ["'microsoft corp'"]
for row in data:   
	#print "c_id : %s\t c_name: %s" % (row[0], row[1])
	for i in range(1993,2017):
		for quarter in range(1,5):
			query = "python sec_ftp_fetch.py %s %s %s" % (row, i, quarter)
			os.system(query)
#cursor.close()

#db.close()
#sys.exit()
