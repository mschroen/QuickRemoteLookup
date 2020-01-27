#!python

import os, sys

# Set default config file or get it from argument
config_file = os.path.dirname(os.path.realpath(__file__)) + '/mynotes.cfg'
if len(sys.argv) > 1:
    if os.path.isfile(sys.argv[1]):
        config_file = sys.argv[1]
#print('| Reading config from '+ config_file) # verbose info
 
# Read config or die
from configobj import ConfigObj
try:
    config = ConfigObj(config_file, encoding="cp850")
except:
    print('= Sorry, something went wrong with the config file:' + config_file)
    sys.exit()

print('QuickRemoteLookup in '+ config['user'] +'@'+ config['server'] +':'+ config['file'])

# Password
import getpass
pswd = getpass.getpass(prompt='> Password: ')

# Connect
import ftplib
from io import BytesIO

try:
    print('| Connecting... ', end='')
    remote = ftplib.FTP_TLS(config['server'])
    print('Server OK.. ', end='')

    remote.login(config['user'], pswd)
    print('Login OK.. ', end='')

    remote.prot_p() # Enables secure communication, prerequisit for some providers
    print('Encryption OK.')

    print('< Receiving file... ', end='')
    memory = BytesIO()
    remote.retrbinary("RETR " + config['file'], memory.write)
    print('%.f Bytes.' % memory.getbuffer().nbytes)
    
except ftplib.all_errors as e:
    print(str(e))
    print('= Sorry.')
    sys.exit()

remote.close()
print('= Connection closed.')

while 1:
    print('> ', end='')
    s = str(input())
    if not s: break
    memory.seek(0)
    for l in memory:
        if s.lower() in str(l).lower():
            print(l.decode("utf-8").rstrip())

print('= Ciao!')