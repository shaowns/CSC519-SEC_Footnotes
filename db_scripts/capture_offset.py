#!/usr/bin/python

import os
import MySQLdb
import re

doc_path = "../resources/doc/"
doc_array = os.listdir(doc_path)
suffixes = ('.txt')
for doc in doc_array[:]:
    if doc.endswith(suffixes) == False:
      doc_array.remove(doc)

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

for doc in doc_array[:]:
	file_name = doc.split('.')[0]
	split_file = file_name.split('_')
	#file_type = split_file[0]
	year = split_file[0]
	quarter = split_file[1][1:]
	file_name = '_'.join(split_file[2:])
	c_id = companies[c_name]
	file_info_query = "SELECT file_id from files_info where c_id = %s and year = %s and quarter = %s" % (c_id, year, quarter)
	cursor.execute(file_info_query)
	f_id = cursor.fetchall()[0][0]
	#print f_id
	#f_id = ""
	#start_os=0
	#end_os=0
	doc_name = doc_path + doc
	with open(doc_name, 'r') as ifile:
		content = ifile.read()
		start_os = content.index('1acbf042c3fe4cc920e075f47dceca01')
		end_os = content.index('b73a4f109926f7ba8c2f646b0fbd6a62')
		increment_query = "SELECT AUTO_INCREMENT from information_schema.tables where table_schema='sec' and table_name='offsets'"
		cursor.execute(increment_query)
		count = cursor.fetchall()
		count = count[0][0]
		print count, f_id, start_os, end_os
		insert_query = "insert ignore into offsets values(%s, %s, %s, %s)" % (count, f_id, start_os, end_os)
		#print insert_query
		cursor.execute(insert_query)
