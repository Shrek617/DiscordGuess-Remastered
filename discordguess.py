import requests
import json
import logging
import time
from time import sleep
from colorama import init, Fore

init()

print(Fore.LIGHTGREEN_EX + """
    ____  _                          ________                    
   / __ \\(_)_____________  _________/ / ____/_  _____  __________
  / / / / / ___/ ___/ __ \\/ ___/ __  / / __/ / / / _ \\/ ___/ ___/
 / /_/ / (__  ) /__/ /_/ / /  / /_/ / /_/ / /_/ /  __(__  |__  ) 
/_____/_/____/\\___/\\____/_/   \\__,_/\\____/\\__,_/\\___/____/____/  Remastered  
                                                                 """ + Fore.RESET);

# Discord has a 10 requests/minute rate limit on the Add Friend function.
# Rate limiting delays are implemented, but use a 15 second delay to avoid suspicion.

token = input('Token: ')      # Discord Authorization Token
delay = int(input('Delay [Rec. 15]: ')) # Seconds to wait between requests
number = int(input('Number: ')) # Number to check tag
totalnumber = number + 1
print(Fore.LIGHTGREEN_EX + str(number) + '+' + '1' + '=' + str(totalnumber) + ' ' + '(Total Number)' + Fore.RESET)
req = {}
req['username'] = input('Username: ') # Username to guess
token = token.replace('"', '')

headers = { 'Host':             'discordapp.com',
            'User-Agent':       'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept':           '*/*',
            'Accept-Language':  'en-GB',
            'Accept-Encoding':  'gzip, deflate, br',
            'Content-Type':     'application/json',
            'Authorization':    token,
            'Connection':       'keep-alive',
            'Referer':          'https://discordapp.com/channels/@me'}

# Grab necessary cookies
s = requests.Session()
s.get('https://discordapp.com/channels/@me')
print('Cookies -->', s.cookies.get_dict())
print()

# Logging setup
formatter = logging.Formatter('%(message)s') 
def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Logging
named_tuple = time.localtime() # Time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple) # Time
logger = setup_logger('log', 'log.txt')
logger.info('New session started - ' + time_string)
logger.info('Username: ' + req['username'])
logger.info('Total Number: ' + str(totalnumber))
logger.info('Delay: ' + str(delay))
super_logger = setup_logger(req['username'], req['username'] + '.txt')

# Start bruteforce
found = False
i = number                              
while i<1000:
    normalSleep = True
    i += 1
    print('[',i,'] ', sep = '', end = '')
    req['discriminator'] = i
    check = str(i)
    with open(req['username'] + '.txt') as f:
        match = check in f.read().splitlines()
    if match == True: # Prevent Ban | Two friend request sent = ban
        print(Fore.LIGHTGREEN_EX + 'Ignoring because this Discord Tag in success list.' + Fore.RESET)
        print('Discord Tag: ', Fore.LIGHTBLUE_EX + req['username'], '#', i, sep = '' + Fore.RESET)
    if match != True:
        r = s.post('https://discordapp.com/api/v6/users/@me/relationships', data = json.dumps(req), headers = headers)
        if r.status_code == 204:   # Friend Request sent
            print(Fore.LIGHTGREEN_EX + 'Success! Now im ignoring this Discord Tag to prevent ban. Dont delete or redacting ' + req['username'] + '.txt ' + 'file to prevent ban' + Fore.RESET)
            logger.info('[' + str(i) + '] ' + 'Success! Now im ignoring this Discord Tag to prevent ban. Dont delete or redacting ' + req['username'] + '.txt ' + 'file to prevent ban')
            print('Discord Tag: ', Fore.LIGHTBLUE_EX + req['username'], '#', i, sep = '' + Fore.RESET)
            super_logger.info(str(i))
            found = True
        elif r.status_code == 400: # Incorrect Discriminator
            print('Incorrect')
            print(Fore.LIGHTRED_EX + 'This Discord Tag doesn\'t exist.' + Fore.RESET)
            logger.info('[' + str(i) + '] ' + 'Incorrect')
        elif r.status_code == 429: # Rate Limit
            i -= 1
            p = (json.loads(r.text)['retry_after'])/1000
            print(Fore.MAGENTA + 'Rate limit: retrying after', p, 'seconds.' + Fore.RESET)
            logger.warning('[' + str(i) + '] ' + 'Rate limit: retrying after ' + p + ' seconds.')
            normalSleep = False
            sleep(p)
        elif r.status_code == 401: # Invalid token
            print(Fore.LIGHTRED_EX + 'Invalid Token!')
            logger.error('[' + str(i) + '] ' + 'Invalid Token!')
            break
        else:
            print('Unknown error', r.status_code,'-->',r.text)
            logger.error('[' + str(i) + '] ' + 'Unknown error')
    if normalSleep:
        sleep(delay)

print()
