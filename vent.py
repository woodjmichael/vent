import sys
import requests
import csv
import json

payload = {'day': '2018-01-01'}
baseUri = 'https://solaflect-uplink-east.azurewebsites.net/api/v2/'

headers = {'Authorization' : 'Bearer 4615dca0-ba2e-45ff-afc9-e8e2b3cf401b'}

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def pull_machines():
    uri = baseUri + 'machines/'
    r = requests.get(uri, headers=headers)
    
    #print(r.status_code)
    #print(r.headers['content-type'])  
    
    j = r.json() 

    file = open('machines.csv', 'w')
    
    for row in j:
        sn = row['serialNumber']
        type = row['coordinatorType']
        file.write(sn + ',' + type + '\n')
                
    file.close() 
    
    print('Pull machines complete')

def analyze_machines(date):
    try:
        uri = baseUri + 'machines/'
        r = requests.get(uri, headers=headers)
        
        #print(r.status_code)
        #print(r.headers['content-type'])  
        
        j = r.json() 

        file = open('machines.csv', 'w')
        
        for row in j:
            sn = row['serialNumber']
            type = row['coordinatorType']
            file.write(sn + ',' + type + '\n')
            analyze_log(row['serialNumber'], date, type)
            print(date + ' ' + sn + ' complete')
            
        file.close()        

    except requests.HTTPError as e:
      print("HTTP Error: {}".format(e))
    except requests.ConnectTimeout as e:
      print("The request timed out while trying to connect to the remote server: {}".format(e))
    except requests.ConnectionError as e:
      print("Connection Error: {}".format(e))
    except requests.RequestException as e:
      print("Unhandled exception: {}".format(e))
    


def analyze_log(sn, date, type):
    try:
        uri = baseUri + 'machines/' + sn + '/logs'
        payload['day'] = date
        r = requests.get(uri, headers=headers, params=payload)
        
        #print(r.status_code)
        #print(r.headers['content-type'])  
        
        j = r.json()
        
        print(json.dumps(j, indent=4, sort_keys=TRUE))

        file = open('log.csv', 'w')
        
        for row in j:
            file.write(row['CsvLine'])
            file.write('\n')
            
        file.close()
        
        log_csv = csv.reader(open('log.csv'), delimiter=',')
        
        output = open('output.csv', 'a')
        output.write('sn,stc-time,windP\n')
        
        prevVal = 2
        currentVal = 0
                
        if type == 'Erasmo':
            for row in log_csv:
                if (len(row) >= 30) and represents_int(row[30]):
                    currentVal = int(row[30])              
                    if currentVal == 2 and prevVal != 2:
                        output.write(sn + ',' + row[1] + ',' + row[21] + '\n')
                    prevVal = currentVal
        
        if type == 'SecondGen':
            for row in log_csv:
                if (len(row) >= 12) and represents_int(row[12]):
                    currentVal = int(row[12])
                    if currentVal == 2 and prevVal != 2:
                        output.write(sn + ',' + row[1][7:15] + ',' + row[23] + '\n')
                    prevVal = currentVal
                        
        output.close()
                        
             

    except requests.HTTPError as e:
      print("HTTP Error: {}".format(e))
    except requests.ConnectTimeout as e:
      print("The request timed out while trying to connect to the remote server: {}".format(e))
    except requests.ConnectionError as e:
      print("Connection Error: {}".format(e))
    except requests.RequestException as e:
      print("Unhandled exception: {}".format(e))

      
      
      
output = open('output.csv', 'w')      
output.write('')
output.close

if len(sys.argv) > 1:
    if sys.argv[1] == '-pm':
        pull_machines()

    elif sys.argv[1] == '-am':
        analyze_machines(str(sys.argv[2])) # date
    
    elif sys.argv[1] == '-al':
        analyze_log(str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4])) # sn, date, type
else:    
    analyze_machines('2018-04-04')
    analyze_machines('2018-04-05')
  
print("Hey it worked! (stop celebrating and get to work)")