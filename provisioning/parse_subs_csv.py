#!/usr/bin/python

import csv, sys, os
import numpy

csvfiles = ['/Users/dataylor/Downloads/Delta_Air_Lines_inventory_report-evpla999.csv','/Users/dataylor/Downloads/Delta_Air_Lines_inventory_report-sdc1mgm01-sat01.csv']
deltainuse = '/Users/dataylor/Downloads/Delta Account #525786.csv'
#csvfiles = sys.argv(1)

def readMyFile(filenames):
    uuids = []
    hostnames = []
    subscriptions = []
    amounts = []
    account_num = []
    contract_num = []
    start_date = []
    end_date = []
    phys_cpu = []
    cores = []
    virtual = []
    hypervisor = []
    unlicensed_hosts = []
    shortarr = []
    for filename in filenames:
		#with open(filename, "rb") as infile, open("%s_unlicensed.csv" % filename, "wb") as outfile:
		with open(filename, "rb") as infile:
		    csvReader = csv.reader(infile)
		    header = next(csvReader, None)
		    #writer = csv.writer(outfile)
	            for row in csvReader:
	        	if row[6] != 'unknown' and row[6] != '':
		            uuids.append(row[0])
		            hostnames.append(row[1])
		            subscriptions.append(row[3])
		            amounts.append(row[4])
		            account_num.append(row[5])
		            contract_num.append(row[6])
		            start_date.append(row[7])
		            end_date.append(row[8])
		            phys_cpu.append(row[9])
		            cores.append(row[10])
		            virtual.append(row[11])
		            hypervisor.append(row[12])
                            short = "%s" % row[3].replace(' ','-').replace('(','').replace(')','-').replace(',','')
                            shortarr.append(short)
                            lin_outfile = "%s_hosts.csv" % short
                            shell = os.system("if [ ! -e '%s' ] ; then echo '%s' > %s ; fi" % (lin_outfile,header,lin_outfile))
                            with open(lin_outfile, "a") as outfile:
                               writer = csv.writer(outfile)
		               #writer.writerow([row[1],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]])
		               writer.writerow(row)
		        else:
		        	unlicensed_hosts.append(row[1])
                                unlin_outfile = "unlicensed_hosts.csv"
                                with open(unlin_outfile, "a") as outfile:
                                  writer = csv.writer(outfile)
		        	  writer.writerow([row[1]])
    return uuids, hostnames, subscriptions, amounts, account_num, contract_num, start_date, end_date, phys_cpu, cores, virtual, hypervisor, unlicensed_hosts, shortarr
 
 
uuids, hostnames, subscriptions, amounts, account_num, contract_num, start_date, end_date, phys_cpu, cores, virtual, hypervisor, unlicensed_hosts, shortarr = readMyFile(csvfiles)

print "number of subscriptions in use: %d" % len(subscriptions)
print "number of licensed hosts: %d" % len(hostnames)
print "number of unlicensed hosts: %d" % len(unlicensed_hosts)
print "number of unique subscriptions: %d" % len(numpy.unique(subscriptions))
print "list of unique subscriptions:"
usub = []
for sub in subscriptions:
  if sub not in usub:
    usub.append(sub)

for uniq in usub:
  print uniq

usub = []
print "number of unique, licensed hostnames: %d" % len(numpy.unique(hostnames))
print "number of unique contract numbers: %d" % len(numpy.unique(contract_num))
print "list of unique contracts:"
for sub in contract_num:
  if sub not in usub:
    usub.append(sub)

for uniq in usub:
  print uniq

print "number of unique account numbers: %d" % len(numpy.unique(account_num))
print "list of unique account numbers:"
usub = []
for sub in account_num:
  if sub not in usub:
    usub.append(sub)

for uniq in usub:
  print uniq

usub = []
print "Subscription counts"
for sub in shortarr:
  if sub not in usub:
    usub.append(sub)
    filename = "%s_hosts.csv" % sub
    with open(filename, "rb") as infile:
      csvReader = csv.reader(infile)
      next(csvReader, None)
      count = []
      for row in csvReader:
        count.append(row)
    print "subscription %s has %d servers attached" % (sub,len(count))

usub = []
print "Subscription counts by contract"
for sub in subscriptions:
  if sub not in usub:
    usub.append(sub)
    short = "%s" % sub.replace(' ','-').replace('(','').replace(')','-').replace(',','')
    filename = "%s_hosts.csv" % short
    ucontract = []
    for contract in contract_num:
      if contract not in ucontract:
        ucontract.append(contract)
        exec("contract_%s = []" % contract)
        with open(filename, "rb") as infile:
          csvReader = csv.reader(infile)
          next(csvReader, None)
          count = []
          for row in csvReader:
            if row[3] == sub and row[6] == contract:
              count.append(row)
          if len(count) != 0:
            print "contract %s, subscription %s has %d servers attached" % (contract,sub,len(count))
            exec("contract_%s.append(row)" % contract)
#        attached = len(count)
#        with open(deltainuse) as infile:
#          csvReader = csv.reader(infile)
#          next(csvReader, None)
#          count = []
#          for row in csvReader:
#            if row[3] == sub:
#              avail = row[4] - attached
#              print "contract %s, subscription %s has %d total, %d in use, %d available" % (contract, sub, row[4], attached, avail) 

