# XIQ PoE Check
### XIQ_PoE_Check.py
## Purpose
This script will collect Power Status for each device of a particular building. Once collect the script will export a CSV listing the device names with their current power status.

## Information
##### Collecting Devices
When running the script, you will be prompted to enter a building name. The script will then collect devices for each floor within that building. The script will filter out a list of devices that are currently connected to XIQ. 

## Needed files
The XIQ_PoE_Check.py script uses several other files. If these files are missing the script will not function.
In the same folder as the XIQ_PoE_Check.py script there should be an /app/ folder. Inside this folder should be a logger.py file and a xiq_api.py file. After running the script a new file 'staggered_reboot.log' will be created.

The log file that is created when running will show any errors that the script might run into. It is a great place to look when troubleshooting any issues.

## Running the script
open the terminal to the location of the script and run this command.

```
python XIQ_Staggered_Reboot.py
```
### Logging in
The script will prompt the user for XIQ credentials.
>Note: your password will not show on the screen as you type

### flags
There is an optional flag that can be added to the script when running.
```
--external
```
This flag will allow you to create the locations and assign the devices to locations on an XIQ account you are an external user on. After logging in with your XIQ credentials the script will give you a numeric option of each of the XIQ instances you have access to. Choose the one you would like to use.

You can add the flag when running the script.
```
python XIQ_Staggered_Reboot.py --external
```
## requirements
There are additional modules that need to be installed in order for this script to function. They are listed in the requirements.txt file and can be installed with the command 'pip install -r requirements.txt' if using pip.