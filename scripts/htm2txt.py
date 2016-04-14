#!/usr/bin/python

import os
import re
import html2text

doc_path = "../resources/doc/"
doc_array = os.listdir(doc_path)
prefixes = ('f_', 'm_')
suffixes = ('.txt')
for doc in doc_array[:]:
	if doc.startswith(prefixes) == False:
		if doc.endswith(suffixes) == False:
			doc_array.remove(doc)
for doc in doc_array[:]:
	htm_doc = doc_path + doc
	pre, ext = os.path.splitext(htm_doc)
	txt_doc = pre + ".txt"
	try:
		os.stat(txt_doc)
		if os.stat(txt_doc).st_size == 0:
			raise Exception("empty txt file %s, so recreating!" % txt_doc)
	except:
		with open(htm_doc, 'r') as ifile, open(txt_doc, 'w') as ofile:
			content = ifile.read()
			content = html2text.html2text(content)
			content = content.encode('ascii', 'ignore')
			ofile.write(u'%s' % content)
		os.remove(htm_doc)
