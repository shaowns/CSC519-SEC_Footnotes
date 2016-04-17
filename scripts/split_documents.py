#!/usr/bin/python

import os
import re
from bs4 import BeautifulSoup, SoupStrainer

doc_path = "../resources/doc/"
cur_doc = ""
toc = "#toc"
actual_link = ""
next_link = ""
file_content = ""
start = 0
end = 0

link_match = re.compile(r"^([\s\Sa-zA-Z]*)(?:Notes)(?: to)([\sa-zA-Z]*)(Statements)$")

doc_array = os.listdir(doc_path)
prefixes = ('f_', 'm_')

for doc_name in doc_array[:]:
	if doc_name.startswith(prefixes):
		doc_array.remove(doc_name)
for doc_name in doc_array[:]:
	if cur_doc != "":
		os.remove(cur_doc)
	cur_doc = doc_path+doc_name
	cur_doc_f = doc_path + "f_" + doc_name
	cur_doc_m = doc_path + "m_" + doc_name
	with open(cur_doc, 'r') as f:
		file_content = f.read()
		links = BeautifulSoup(file_content, "html5lib").findAll('a')
		for link in links:
			if actual_link == "" and link.has_attr('href') and link['href'] != toc:
				if link_match.match(link.text.strip().encode('ascii','ignore')):
					print link
					actual_link = link['href'][1:]
					print actual_link
			else:
				if next_link == "" and link.has_attr('href') and link['href'] != toc:
					next_link = link['href'][1:]
		footnote_start_pattern = r'<a name="%s">' % actual_link
		next_flag = 0
		file_content = file_content.replace('<A NAME="%s">' % actual_link,'<A NAME="%s">%s' % (actual_link, "a02506b31c1cd46c2e0b6380fb94eb3d"))
		for link in links:
			if next_flag == 1 and link.has_attr('name'):
				next_link = link['name']
				break
			else:
				if link.has_attr('name') and link['name'] == actual_link:
					next_flag = 1
		file_content = file_content.replace('<A NAME="%s">' % next_link,'<A NAME="%s">%s' % (next_link, "a02506b31c1cd46c2e0b6380fb94eb3d"))
		#footnote_end_pattern = r'<a name="%s"></a>' % next_link
		#footnote_start_match = re.search(footnote_start_pattern, file_content, re.IGNORECASE)
		#footnote_end_match = re.search(footnote_end_pattern, file_content, re.IGNORECASE)
		#start = footnote_start_match.start()
		#end = footnote_end_match.end()
		#target_html = file_content[start:end]
		
	#try:
	#	os.stat(cur_doc_f)
	#except:
	with open(cur_doc, 'w') as fn:
		fn.write(file_content)
	#with open(cur_doc, 'r') as ifile, open(cur_doc_m, 'w') as ofile:
	#	ofile.write(ifile.read(start))
	#	ifile.seek(end)
	#	ofile.write(ifile.read())
#if cur_doc != "":
#	os.remove(cur_doc)


