import praw
import os, sys, time
import datetime as dt
from random import randint
from roller import *
from errors import *

# TO DO LIST
# - Add advantage/disadvantage rolls
# - Keep track of users in a database, log rolls there
# - Allow whitelisted users to award inspiration points to others

####################################
#                                  #
#         DICEBOT SETTINGS         #
#                                  #
####################################

# These settings can be changed freely, keep in mind that 'True' and 'False' are case-sensitive!

# Admin Settings
bot_managers = [   # These users will be messaged in the event of a critical error or bot crash
    'Nose_Fetish', # Please do not remove me! I need to know when bad errors happen :)
    'aceavengers', # Add new usernames separated by commas (and inside the brackets)
]

# Error Handling
error_reply =       True # Reply to users when their roll fails (Default: True)
error_dm =          False # DM users when their roll fails (Default: False)

####################################
#         BOT SETTINGS END         #
####################################
# Not a good idea to modify anything below here, or in 'parser.py' or 'errors.py'
# If you want something changed that isn't in the settings above, message me!

# FUNCTIONS
def get_timestamp():
    return str(dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

# REDDIT INSTANCE
reddit = praw.Reddit(
    client_id='6J61rYtJNMLj9w',
    client_secret='yam8U2tAXY6X02369hMRyqH9kQNTZQ',
    user_agent='<console:DRB:1.0.0>',
    username='_dice_bot',
    password='Valuecharm1001$'
)

# BOT START
start_time = get_timestamp()
print(f'\n[ DiceBot is online at {start_time} ]')

comment = "Hey /u/_dice_bot roll me some fuckin dice -- I want [1d20-2 to hit] and [2d8+4 damage] and I want it NOW"
#comment = "This message has no commands in it. Har har har."

#print(f"INPUT: {comment}")

lexer = Lexer(comment)
tokens, error = lexer.tokenize()
if error: print(error.as_string())

#print(f"TOKENS: {tokens}")

parser = Parser(tokens)
rolls, error = parser.parse()
if error: print(error.as_string())

print(rolls)
sys.exit(0)

interpreter = Interpreter()
result, error = interpreter.visit(rolls)
if error: print(error.as_string())

print(result)

# CHECK INBOX LOOP
#while True:
#    try:
#        for message in reddit.inbox.unread(limit=25):
#            if 'u/_dice_bot' in str(item.body):
#                timestamp = get_timestamp()
#                comment = item.body.lower()
#
#                lexer = Lexer(comment)
#                tokens, error = lexer.tokenize()

#                parser = Parser(tokens)
#                response, error = parser.parse()
#                if error: print(error)
#                else:
#                    print(f"[{timestamp}] {response}")
#                    sys.exit()
