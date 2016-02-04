#!/usr/bin/python
#Arguments :
# "company" - full company name enclosed in quotes
# year - the year you want to check the filings for
# quarter - the quarter you want to check filings for

import sys
import os
import ftplib

argc = len(sys.argv)
argv = sys.argv
company = argv[1]
year = argv[2]
qtr = argv[3]
ftp = ftplib.FTP('ftp.sec.gov', 'anonymous','')
path = 'edgar/full-index/' + year + '/QTR' + qtr
resource_path = os.pardir + '/resources/'
year_path = resource_path + year
local_path = year_path + '/QTR' + qtr
local_file = local_path + '/company.idx'

#make resources directory if not found

try:
  os.stat(resource_path)
except:
  os.mkdir(resource_path)

#make directory for year if not found

try:
  os.stat(year_path)
except:
  os.mkdir(year_path)

#make directory for quarter if not found

try:
  os.stat(local_path)
except:
  os.mkdir(local_path)

ftp.cwd(path)

#fetch file from ftp server if not found

try:
  os.stat(local_file)
except:
  ftp.retrbinary("RETR " + 'company.idx',open(local_file, 'wb').write)

company_dict = {}

#read from .idx file and create dictionary

with open(local_file, 'r') as f:
  for _ in xrange(10):
    next(f)
  for line in f:
    output = [s.strip() for s in line.split('  ') if s]
    output[0] = output[0].lower()
    if output[1] == '10-Q':
      company_dict[output[0]] = {}
      company_dict[output[0]][output[1]] = output[4]
    else:
      continue

#fetch required filing from ftp server

try:
  print company_dict[company]['10-Q']
except:
  print company + " : No filing found"
