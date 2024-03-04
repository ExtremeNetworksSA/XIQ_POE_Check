#!/usr/bin/env python3
import logging
import argparse
import sys
import os
import re
import inspect
import getpass
import pandas as pd
from app.logger import logger
from app.xiq_api import XIQ
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
logger = logging.getLogger('PoE_Check.Main')

XIQ_API_token = ''

pageSize = 100

parser = argparse.ArgumentParser()
parser.add_argument('--external',action="store_true", help="Optional - adds External Account selection, to use an external VIQ")
args = parser.parse_args()

PATH = current_dir

# Git Shell Coloring - https://gist.github.com/vratiu/9780109
RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
RESET = "\033[0;0m"

def yesNoLoop(question):
    validResponse = False
    while validResponse != True:
        response = input(f"{question} (y/n) ").lower()
        if response =='n' or response == 'no':
            response = 'n'
            validResponse = True
        elif response == 'y' or response == 'yes':
            response = 'y'
            validResponse = True
        elif response == 'q' or response == 'quit':
            sys.stdout.write(RED)
            sys.stdout.write("script is exiting....\n")
            sys.stdout.write(RESET)
            raise SystemExit
    return response

if XIQ_API_token:
    x = XIQ(token=XIQ_API_token)
else:
    print("Enter your XIQ login credentials")
    username = input("Email: ")
    password = getpass.getpass("Password: ")
    x = XIQ(user_name=username,password = password)

#OPTIONAL - use externally managed XIQ account
if args.external:
    accounts, viqName = x.selectManagedAccount()
    if accounts == 1:
        validResponse = False
        while validResponse != True:
            response = input("No External accounts found. Would you like to import data to your network?")
            if response == 'y':
                validResponse = True
            elif response =='n':
                sys.stdout.write(RED)
                sys.stdout.write("script is exiting....\n")
                sys.stdout.write(RESET)
                raise SystemExit
    elif accounts:
        validResponse = False
        while validResponse != True:
            print("\nWhich VIQ would you like to import the floor plan and APs too?")
            accounts_df = pd.DataFrame(accounts)
            count = 0
            for df_id, viq_info in accounts_df.iterrows():
                print(f"   {df_id}. {viq_info['name']}")
                count = df_id
            print(f"   {count+1}. {viqName} (This is Your main account)\n")
            selection = input(f"Please enter 0 - {count+1}: ")
            try:
                selection = int(selection)
            except:
                sys.stdout.write(YELLOW)
                sys.stdout.write("Please enter a valid response!!")
                sys.stdout.write(RESET)
                continue
            if 0 <= selection <= count+1:
                validResponse = True
                if selection != count+1:
                    newViqID = (accounts_df.loc[int(selection),'id'])
                    newViqName = (accounts_df.loc[int(selection),'name'])
                    x.switchAccount(newViqID, newViqName)
                    logger.info(f"Logged into {newViqName}")

# collect building name from user and get ids for any floors of the building
building_search = True
while building_search:
    building = input("Please enter the name of the building: ")
    print("Collecting Location information")
    floor_list = x.getFloors(building)
    if 'errors' in floor_list:
        errors = ", ".join(floor_list['errors'])
        print(errors)
        logger.error(errors)
        yesNoLoop = "would you like to try again?"
        if yesNoLoop == 'n':
            print("script is exiting....")
            raise SystemExit
        print('\n')
    else:
        building_search = False


#Check floor list
if not floor_list:
    msg = f"There was no floors associated with the building {building}"
    print(msg)
    logger.warning(msg)
    print("script is exiting....")
    raise SystemExit
    

device_data = []
for floor in floor_list:
    print(f"Collecting Devices for floor '{floor['name']}'...")
    ## Collect Devices
    temp_data = x.collectDevices(pageSize,location_id=floor['id'])
    device_data = device_data + temp_data

print("\n\n")

if not device_data:
    msg = "There were no devices found!"
    logger.warning(msg)
    print(msg)
    print("script is exiting....")
    raise SystemExit

msg = f"Collected {len(device_data)} APs from location {building}"
print(msg)
logger.info(msg)

# convert device_data dict to dataframe
device_df = pd.DataFrame(device_data)
device_df.set_index('id',inplace=True)
# get list of device ids for cli command call
id_list = [sub['id'] for sub in device_data ]

commands = ['show system power status']
if id_list:
    csv_df = pd.DataFrame(columns = ['Device', 'Power Status'])
    rawData = x.sendCLI(id_list, commands)
    for device_id in rawData['device_cli_outputs']:
        print(rawData['device_cli_outputs'][device_id])
        output = rawData['device_cli_outputs'][device_id][0]['output']
        output_regex = re.compile(r'System\sPower\sStatus:\s+(\w+)')
        power_status = output_regex.findall(output)[0]
        devicename = device_df.loc[int(device_id),'hostname']
        #print(devicename, power_status)
        temp_df = pd.DataFrame([{'Device': devicename, 'Power Status': power_status}])
        csv_df = pd.concat([csv_df, temp_df], ignore_index=True)

print("\n")
print(csv_df)
filename = f"{building}_PoE_Check.csv"
print(f"Writing CSV File {filename}")
csv_df.to_csv(f"{PATH}/{filename}", index=False)