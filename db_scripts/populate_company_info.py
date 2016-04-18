#!/usr/bin/python

import os
import MySQLdb
import re

doc_path = "../resources/doc/"
doc_array = os.listdir(doc_path)

suffixes = (".txt")

db = MySQLdb.connect("localhost", "n3o", "n3o", "sec")
cursor = db.cursor()
companies_query = "SELECT * FROM companies"
cursor.execute(companies_query)
data = cursor.fetchall()
companies = {}
for each in data:
	c_name = each[1]
	c_name = re.sub('[,./]', '', c_name).lower().replace(' ', '_')
	companies[c_name] = each[0]
count=1
for doc in doc_array[:]:
	if doc.endswith(suffixes):
		file_name = doc.split('.')[0]
		split_file = file_name.split('_')
		#file_type = split_file[0]
		year = split_file[0]
		quarter = split_file[1][1:]
		file_name = '_'.join(split_file[2:])
		c_id = companies[file_name]
		print year, quarter, file_name
		increment_query = "SELECT AUTO_INCREMENT from information_schema.tables where table_schema='sec' and table_name='files_info'"
		cursor.execute(increment_query)
		count = cursor.fetchall()
		count = count[0][0]
		select_query = "SELECT * from files_info where c_id = %s and year = %s and quarter = %s" % (c_id, year, quarter)
		cursor.execute(select_query)
		res = cursor.fetchall()
		if res == ():
			insert_query = "INSERT INTO files_info VALUES(%s, %s, %s, %s)" % (count, c_id, year, quarter)
			cursor.execute(insert_query)
		else:
			print "%s already in db" % doc
