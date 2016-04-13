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
link_match = re.compile(r"^[nN]otes(?: to)(?: [a-zA-Z]*)(?: [sS]tatements)")
doc_array = os.listdir(doc_path)
prefixes = ('f_', 'm_')
for doc_name in doc_array[:]:
	if doc_name.startswith(prefixes):
		doc_array.remove(doc_name)
for doc_name in doc_array:
	if cur_doc != "":
		os.remove(cur_doc)
	cur_doc = doc_path+doc_name
	cur_doc_f = doc_path + "f_" + doc_name
	cur_doc_m = doc_path + "m_" + doc_name
	with open(cur_doc, 'r') as f:
		file_content = f.read()
		for link in BeautifulSoup(file_content, "html.parser", parse_only=SoupStrainer('a')):
			if actual_link == "" and link.has_attr('href') and link['href'] != toc:
				if link_match.match(link.contents[0].strip()):
					actual_link = link['href'][1:]
			else:
				if next_link == "" and link.has_attr('href') and link['href'] != toc:
					next_link = link['href'][1:]
		footnote_start_pattern = r'<a name="%s"></a>' % actual_link
		footnote_end_pattern = r'<a name="%s"></a>' % next_link
		footnote_start_match = re.search(footnote_start_pattern, file_content, re.IGNORECASE)
		footnote_end_match = re.search(footnote_end_pattern, file_content, re.IGNORECASE)
		start = footnote_start_match.start()
		end = footnote_end_match.end()
		target_html = file_content[start:end]
		
	try:
		os.stat(cur_doc_f)
	except:
		with open(cur_doc_f, 'w') as fn:
			fn.write(target_html)
	with open(cur_doc, 'r') as ifile, open(cur_doc_m, 'w') as ofile:
		ofile.write(ifile.read(start-1))
		ifile.seek(end)
		ofile.write(ifile.read())
if cur_doc != "":
	os.remove(cur_doc)


