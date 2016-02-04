#!/usr/bin/python
# python filename year quarter

import sys
import os
import ftplib

argc = len(sys.argv)
argv = sys.argv
print argv[1]
ftp = ftplib.FTP('ftp.sec.gov', 'anonymous','')
path = 'edgar/full-index/' + argv[1] + '/QTR' + argv[2]
year_path = os.pardir + '/resources/' + argv[1]
local_path = os.pardir + '/resources/' + argv[1] + '/QTR' + argv[2]
local_file = local_path + '/company.idx'
try:
  os.stat(year_path)
except:
  os.mkdir(year_path)
try:
  os.stat(local_path)
except:
  os.mkdir(local_path)
ftp.cwd(path)
ftp.retrbinary("RETR " + 'company.idx',open(local_file, 'wb').write)
