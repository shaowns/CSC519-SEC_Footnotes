#!/usr/bin/python

import os
import re
import html2text
import codecs
doc_path = "../resources/doc/"
cp1252 = {

    u"\x80": u"\u20AC",
    u"\x81": u"\uFFFD",
    u"\x82": u"\u201A",
    u"\x83": u"\u0192",
    u"\x84": u"\u201E",
    u"\x85": u"\u2026",
    u"\x86": u"\u2020",
    u"\x87": u"\u2021",
    u"\x88": u"\u02C6",
    u"\x89": u"\u2030",
    u"\x8a": u"\u0160",
    u"\x8b": u"\u2039",
    u"\x8c": u"\u0152",
    u"\x8d": u"\uFFFD",
    u"\x8e": u"\u017D",
    u"\x8f": u"\uFFFD",
    u"\x90": u"\uFFFD",
    u"\x91": u"\u2018",
    u"\x92": u"\u2019",
    u"\x93": u"\u201C",
    u"\x94": u"\u201D",
    u"\x95": u"\u2022",
    u"\x96": u"\u2013",
    u'\x97': u'\u2014',
    u"\x98": u"\u02DC",
    u"\x99": u"\u2122",
    u"\x9a": u"\u0161",
    u"\x9b": u"\u203A",
    u"\x9c": u"\u0153",
    u"\x9d": u"\uFFFD",
    u"\x9e": u"\u017E",
    u"\x9f": u"\u0178",
    u"\xa0": u"\u00A0",
    u"\xa1": u"\u00A1",
    u"\xa2": u"\u00A2",
    u"\xa3": u"\u00A3",
    u"\xa4": u"\u00A4",
    u"\xa5": u"\u00A5",
    u"\xa6": u"\u00A6",
    u"\xa7": u"\u00A7",
    u"\xa8": u"\u00A8",
    u"\xa9": u"\u00A9",
    u"\xaa": u"\u00AA",
    u"\xab": u"\u00AB",
    u"\xac": u"\u00AC",
    u"\xad": u"\u00AD",
    u"\xae": u"\u00AE",
    u"\xaf": u"\u00AF",
    u"\xb0": u"\u00B0",
    u"\xb1": u"\u00B1",
    u"\xb2": u"\u00B2",
    u"\xb3": u"\u00B3",
    u"\xb4": u"\u00B4",
    u"\xb5": u"\u00B5",
    u"\xb6": u"\u00B6",
    u"\xb7": u"\u00B7",
    u"\xb8": u"\u00B8",
    u"\xb9": u"\u00B9",
    u"\xba": u"\u00BA",
    u"\xbb": u"\u00BB",
    u"\xbc": u"\u00BC",
    u"\xbd": u"\u00BD",
    u"\xbe": u"\u00BE",
    u"\xbf": u"\u00BF",
    u"\xc0": u"\u00C0",
    u"\xc1": u"\u00C1",
    u"\xc2": u"\u00C2",
    u"\xc3": u"\u00C3",
    u"\xc4": u"\u00C4",
    u"\xc5": u"\u00C5",
    u"\xc6": u"\u00C6",
    u"\xc7": u"\u00C7",
    u"\xc8": u"\u00C8",
    u"\xc9": u"\u00C9",
    u"\xca": u"\u00CA",
    u"\xcb": u"\u00CB",
    u"\xcc": u"\u00CC",
    u"\xcd": u"\u00CD",
    u"\xce": u"\u00CE",
    u"\xcf": u"\u00CF",
    u"\xd0": u"\u00D0",
    u"\xd1": u"\u00D1",
    u"\xd2": u"\u00D2",
    u"\xd3": u"\u00D3",
    u"\xd4": u"\u00D4",
    u"\xd5": u"\u00D5",
    u"\xd6": u"\u00D6",
    u"\xd7": u"\u00D7",
    u"\xd8": u"\u00D8",
    u"\xd9": u"\u00D9",
    u"\xda": u"\u00DA",
    u"\xdb": u"\u00DB",
    u"\xdc": u"\u00DC",
    u"\xdd": u"\u00DD",
    u"\xde": u"\u00DE",
    u"\xdf": u"\u00DF",
    u"\xe0": u"\u00E0",
    u"\xe1": u"\u00E1",
    u"\xe2": u"\u00E2",
    u"\xe3": u"\u00E3",
    u"\xe4": u"\u00E4",
    u"\xe5": u"\u00E5",
    u"\xe6": u"\u00E6",
    u"\xe7": u"\u00E7",
    u"\xe8": u"\u00E8",
    u"\xe9": u"\u00E9",
    u"\xea": u"\u00EA",
    u"\xeb": u"\u00EB",
    u"\xec": u"\u00EC",
    u"\xed": u"\u00ED",
    u"\xee": u"\u00EE",
    u"\xef": u"\u00EF",
    u"\xf0": u"\u00F0",
    u"\xf1": u"\u00F1",
    u"\xf2": u"\u00F2",
    u"\xf3": u"\u00F3",
    u"\xf4": u"\u00F4",
    u"\xf5": u"\u00F5",
    u"\xf6": u"\u00F6",
    u"\xf7": u"\u00F7",
    u"\xf8": u"\u00F8",
    u"\xf9": u"\u00F9",
    u"\xfa": u"\u00FA",
    u"\xfb": u"\u00FB",
    u"\xfc": u"\u00FC",
    u"\xfd": u"\u00FD",
    u"\xfe": u"\u00FE",
    u"\xff": u"\u00FF",

}

def remove_non_ascii(text):
    # map cp1252 gremlins to real unicode characters
    if re.search(u"[\x80-\xff]", text):
        def fixup(m):
            s = m.group(0)
            return cp1252.get(s, s)
        if isinstance(text, type("")):
            # make sure we have a unicode string
            text = unicode(text, "iso-8859-1")
        text = re.sub(u"[\x80-\xff]", fixup, text)
    return text

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
		with codecs.open(htm_doc, 'r', encoding='utf-8' ) as ifile, open(txt_doc, 'w') as ofile:
			content = ifile.read()
			ofile.write(html2text.html2text(content))
		os.remove(htm_doc)
