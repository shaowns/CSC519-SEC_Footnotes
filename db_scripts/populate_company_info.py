#!/usr/bin/python

import os
import MySQLdb
import re

doc_path = "../resources/doc/"
doc_array = os.listdir(doc_path)

prefixes = ("f_", "m_")
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
for doc in doc_array[:]:
	if doc.startswith(prefixes):
		if doc.endswith(suffixes):
			file_name = os.path.basename(doc)
			split_file = file_name.split('_')
			file_type = split_file[0]
			year = split_file[1]
			quarter = split_file[2][1:]
			file_name = '_'.join(split_file[3:])
			print file_type, year, quarter, file_name
