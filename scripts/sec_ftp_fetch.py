#!/usr/bin/python
#Arguments :
# "company" - full company name enclosed in quotes
# year - the year you want to check the filings for
# quarter - the quarter you want to check filings for

import sys
import os
import ftplib
import re

argc = len(sys.argv)
argv = sys.argv
company = argv[1]
year = argv[2]
qtr = argv[3]
ftp = ftplib.FTP('ftp.sec.gov', 'anonymous','')
path = 'edgar/full-index/' + year + '/QTR' + qtr
resource_path = os.pardir + '/resources/'
file_prefix = year + '_q' + qtr + '_'
idx_file_name = file_prefix + 'company.idx'
idx_path = resource_path + '/idx' 
idx_file_path = idx_path + '/' + idx_file_name
doc_path = resource_path + '/doc'

#make resources directory if not found

try:
  os.stat(resource_path)
except:
  os.mkdir(resource_path)

#make idx directory if not found

try:
  os.stat(idx_path)
except:
  os.mkdir(idx_path)

#make doc directory if not found

try:
  os.stat(doc_path)
except:
  os.mkdir(doc_path)

ftp.cwd(path)

#fetch file from ftp server if not found

try:
  os.stat(idx_file_path)
  if os.stat(idx_file_path).st_size < ftp.size('company.idx'):
    os.remove(idx_file_path)
    raise Exception("incomplete idx file: %s" % idx_file_path)
except:
  ftp.retrbinary("RETR " + 'company.idx',open(idx_file_path, 'wb').write)

company_dict = {}

#read from .idx file and create dictionary

with open(idx_file_path, 'r') as f:
	for _ in xrange(10):
		next(f)
	for line in f:
		output = [s.strip() for s in line.split('  ') if s]
		output[0] = output[0].lower()
		output[0] = re.sub('[,./]', '', output[0])
		if output[1] == '10-Q' or output[1] == '10-K':
			company_dict[output[0]] = {}
			company_dict[output[0]]['doc'] = output[4]
		else:
			continue

#fetch required filing from ftp server

company = re.sub('[,./]', '', company)
file_name = company.lower().replace(' ','_') + '.htm'

try:
  filing_path = company_dict[company]['doc']
  document = doc_path + '/' + file_prefix + file_name
  try:
    ftp.cwd("~/")
    os.stat(document)
    if os.stat(document).st_size < ftp.size(filing_path):
      os.remove(document)
      raise Exception("Incomplete filing document : %s\n" % document)
    print "filing document %s already retrieved" % document
  except:
    ftp.retrbinary("RETR " + filing_path, open(document, 'wb').write)
    print "filing document %s created" % document
  htm_data = ""
  print "title:"
  with open(document, 'r') as f:
    htm_data = f.read().replace('\n','')
except:
  print file_prefix+file_name + " : No filing found"
