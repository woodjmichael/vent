#
# vent.py
# python 3
#
# Michael Wood
# 2018.4.24
#

import sys
import requests
import csv
import json
import os

payload = {'day': '2018-01-01'}
baseUri = 'https://solaflect-uplink-east.azurewebsites.net/api/v2/'
headers = {'Authorization' : 'Bearer 4615dca0-ba2e-45ff-afc9-e8e2b3cf401b'}

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def pull(whatToPull): #'machines' or 'gateways'
    uri = baseUri + whatToPull +'/'
    r = requests.get(uri, headers=headers)       
    
    j = r.json() 
    
    #print(r.status_code)
    #print(r.headers['content-type'])  
    #print(json.dumps(j, indent=4, sort_keys=True))

    file = open('pull.csv', 'w')
    
    if whatToPull == 'machines':
        for row in j:
            sn = row['serialNumber']
            type = row['coordinatorType']
            file.write(sn + ',' + type + '\n')
    else :
        for row in j:
            netID = row['netid']
            name = row['friendlyName']            
            file.write(str(netID) + ',' + str(name) + '\n')            
                    
    file.close() 
    
    print('Pull ' + whatToPull + ' complete')

def analyze_all_machines(date):   
    machine_csv = csv.reader(open('machine_list.csv'), delimiter=',')
    
    for row in machine_csv:
        if represents_int(row[0][0]) and represents_int(row[2]) :
            analyze_one_machine(row[0], date, row[1], row[2])       #pass: sn, date, type, stowPos
            print(date + ' ' + row[0] + ' complete')                #pass: date, sn
        else :
            print('ERROR: ' + date + ' ' + row[0])


def analyze_one_machine(sn, date, type, stowPosStr):
    try:
        gen = int(sn[0])
        stowPos = int(stowPosStr)
        
        uri = baseUri + 'machines/' + sn + '/logs'
        payload['day'] = date
        r = requests.get(uri, headers=headers, params=payload)
        
        #print(r.status_code)
        #print(r.headers['content-type'])  
        
        j = r.json()               
        
        file = open('log.csv', 'w')
        
        for row in j:
            file.write(row['CsvLine'])
            file.write('\n')
            
        file.close()
        
        log_csv = csv.reader(open('log.csv'), delimiter=',')
                
        output = open('output.csv', 'a')        

        stow = True   
                
        if type == 'Erasmo' or gen != 6:
            for row in log_csv:
                if ((len(row) > 30) and represents_int(row[6])) :                    
                    elpos = int(row[6])
                    if ((elpos >= (stowPos-1000)) and (not stow)) : 
                        stow = True                        
                        output.write(sn + ',' + row[3] + ',' + row[6] + ',' + row[21] + ',' + row[30] + '\n')
                    if ((elpos < (stowPos-1000)) and stow) :
                        stow = False
        
        elif type == 'SecondGen' and gen == 6:
            for row in log_csv:
                if ((len(row) > 23) and represents_int(row[3])) :
                    elpos = int(row[3])                    
                    if ((elpos >= (stowPos-100)) and (not stow)) :
                        stow = True
                        output.write(sn + ',' + row[1][7:15] + ',' + row[3] + ',' + row[23] + ',' + row[12] + '\n')
                    if ((elpos < (stowPos-100)) and stow) :
                        stow = False                                                
        output.close()
                        
             

    except requests.HTTPError as e:
      print("HTTP Error: {}".format(e))
    except requests.ConnectTimeout as e:
      print("The request timed out while trying to connect to the remote server: {}".format(e))
    except requests.ConnectionError as e:
      print("Connection Error: {}".format(e))
    except requests.RequestException as e:
      print("Unhandled exception: {}".format(e))

      
      
      
#
# Main execution      
#     
try:
    os.remove('output.csv')
except OSError:
    pass
            
if len(sys.argv) > 1:
    if sys.argv[1] == '-pm':
        pull('machines')
        
    elif sys.argv[1] == '-pg':
        pull('gateways')
        
    elif sys.argv[1] == '-aam':
        analyze_all_machines(str(sys.argv[2])) #pass: date
    
    elif sys.argv[1] == '-aom':
        #pass: sn, date, type, stowPos
        analyze_one_machine(str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]), str(sys.argv[5]))
else:    
    analyze_all_machines('2018-04-04')
    analyze_all_machines('2018-04-05')
  
print("Hey it worked! (stop celebrating and get to work)")