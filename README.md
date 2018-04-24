# vent #

Michael Wood
2018.4.23
Python 3

Vent analyzes wind event log data.

#Usage:

##No arguments 
fill output.csv with wind event data from hard-coded dates

##-pm 
Pull (list of all) machines into pull.csv, easy hard-coded option to print JSON

##-pg
Pull (list of all) gateays into pull.csv, easy hard-coded option to print JSON

##-aam <yyyy-mm-dd>
Analyze all machines in machine_list.csv for wind events, output to output.csv
- Arg1 = date

##-aom <sn> <yyyy-mm-dd> <Erasmo | SecondGen> <65000 | 3900 | 1900>
Analyze one machine for wind events, output to output.csv
- Arg1 = serial number (needs to match format in Cirrus)
- Arg2 = date
- Arg3 = coordinator type
- Arg4 = stow position (helps define when a machine is actually stowed)