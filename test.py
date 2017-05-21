import json
import os
import urllib
from collections import defaultdict
import collections
import string
import datetime
import sys
import smtplib
from email.mime.text import MIMEText

###########################Fucntion for node check#################################
def recent_node_counts():
    count = 0
    while True:
        count += 1
        try:
            url_node = os.popen("curl -u ** https://api.hanatrial.ondemand.com/monitoring/v1/accounts/services/apps/account/state 2>/dev/null").read()
            node_data = json.loads(url_node)
            if (count > 10):
                print("10 tries commited to connect to API URL")
        except BaseException as exp:
            continue
        break
    process_num = (node_data[0]['processes'])
    node_count = len(process_num)
    f_check = file("/home/service_check/trial/account/node_file.txt",'r')
    f_data = f_check.read()
    chk_data = int(f_data)
    if(node_count > chk_data): ###checks node count from previous file if increased writes the new count to file 
       print (' ')
       print 'Process count increased to = ',  node_count
       print (' ')
       print 'previous process count = ', chk_data
       print (' ')
############################write increased count to file######################################################
       f1 = open("node_file.txt", "w")
       n1 = f1.write(str(node_count) + "\n")
       f1.close()
##########################################send email notification#########################################
    return node_count ### returns recent node counts
    

recent_node_counts()

######################################create Notofication about the failed service ########################     
def service_accounts():
    comp_n = recent_node_counts()
    f2 = file("/home/c5242046/test/node_file.txt",'r') ## reads last value of nodes
    r_data = f2.read()
    cmp_n = int(r_data)
    if(comp_n < cmp_n ):
          print (' ')
	  print 'one or more processes are in failed state'
	  print (' ')
          print 'recent previous count of processes = ', cmp_n
          print (' ')
          print 'currently running number of processes = ', comp_n
          print (' ')
          print ('last changed approx in UTC :' + datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y"))
          print (' ')
################################# SEnd_Email about the failed instances###################################
	  host = 'mail.sap.corp'
          port = 25
          s = smtplib.SMTP(host, port)
          s.ehlo()
          s.starttls
          msg = MIMEText("""One or more processes are in failed state for Service ACCOUNTS\n Console log: https://mo-02ea63e9f.mo.sap.corp:8443/job/Service_check_EU1_Trial/lastUnsuccessfulBuild/console \n Application Dashboard: https://account.hanatrial.ondemand.com/cockpit#/acc/services/app/account/dashboard""")
          sender = 'noreply@exchange.sap.corp'
          recipients = ['indranil.roy@sap.com']
          msg['subject'] = "[NEWTRIAL]:Service:Accounts:One or more processes are in failed state"
          msg['From'] = sender
          msg['text'] = "body of mail"
          msg['To'] = ", ".join(recipients)
          s.sendmail(sender, recipients, msg.as_string())
          s.quit()
          print (' ')
          print "mail sent"
          print (' ')
          sys.exit(1) ### fail the build forcefully if processes are failed
    else:
          print (' ')
          print 'recent count of processes running = ', comp_n
          print (' ')
          print 'All processes are running fine'
          print (' ')
service_accounts()

#def critical_metrics()
    #url_met = "https://**@api.hanatrial.ondemand.com/monitoring/v1/accounts/services/apps/account/state"
    #node_met = json.load(urllib.urlopen(url_node))
    
