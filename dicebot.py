import praw
import os, sys, time
import datetime as dt
from random import randint
from roller import *
from errors import *

# TESTS TO RUN
# zero rolls/die
# no rolls in comment

# Planned Features
# - Advantage/disadvantage rolls
# - Keep track of users in a database, log rolls there
# - Allow whitelisted users to award inspiration points to others
# - Commas in really big numbers
# - "4d6 drop the lowest" for character stats
# - Maybe random character generators with name, class, stats, etc just for fun
# - More descriptive error messages (mentioning which command caused the error)

# Known Bugs to Fix
# - Labels can't contain numbers or symbols of any kind, the lexer just ignores them
# - Empty brackets are given an empty roll response instead of an error
# - Server errors ouput a bunch of nonsense to the console (not fatal)

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

# Format Settings
reply_template =  "*You rolled...*\n\n" # Base template for replies, '\n' is a line break, this also accepts reddit formatting
line_separators = False                 # Put line separators between each roll
bold_rolls =      False                 # Use bold text for rolls
ital_rolls =      False                 # Use italic text for rolls

# Error Handling
retry_wait_time = 60    # Time to wait (in seconds) before retrying after a server connection error
error_reply =     True  # Reply to users when their roll fails (Default: True)
# error_dm =      False # DM users when their roll fails (Default: False) ** NOT IMPLEMENTED **

####################################
#         BOT SETTINGS END         #
####################################
# Not a good idea to modify anything below here, or in 'roller.py', you can edit error messages in 'errors.py'
# If you want something changed that isn't in the settings above, message me!

# FUNCTIONS
def get_timestamp():
    return str(dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

def make_reply():
    output = reply_template
    if line_separators == True: output += '---\n\n'
    for i in range(len(result)):
        if bold_rolls and ital_rolls: output += f'***{result[i]}***' # Bold and italic enabled
        elif bold_rolls: output += f'**{result[i]}**' # Bold enabled
        elif ital_rolls: output += f'*{result[i]}*' # Italic enabled
        else: output += f'{result[i]}' # Bold and italic disabled

        if i < len(result)-1: # For every roll except the last one
            if line_separators: output += '\n\n---\n\n' # Line separators enabled
            else: output += '\n\n' # Line separators disabled

    return output

# REDDIT INSTANCE
reddit = praw.Reddit(
    client_id='6J61rYtJNMLj9w',
    client_secret='yam8U2tAXY6X02369hMRyqH9kQNTZQ',
    user_agent='<console:DRB:1.0.0>',
    username='_dice_bot',
    password='Valuecharm1001$'
)

# CLEAR CONSOLE
try: os.system('clear')
except: os.system('cls')

# BOT START
start_time = get_timestamp()
print(f'\n[ DiceBot is online at {start_time} ] CTRL+C to exit')

# CHECK INBOX LOOP
while True:
    try:
        for item in reddit.inbox.unread(limit=25):
            if 'u/_dice_bot' in str(item.body):
                timestamp = get_timestamp()
                comment = item.body.lower()

                lexer = Lexer(comment)
                tokens, error = lexer.tokenize()
                if error:
                    print(item.id + ': ' + error.as_string())
                    if error_reply: item.reply(error.message) # reply to error comments with details
                    item.mark_read() # mark the error comment as read, then continue
                    continue

                parser = Parser(tokens)
                rolls, error = parser.parse()
                if error:
                    print(item.id + ': ' + error.as_string())
                    try: # most of the time, this error will happen (likely an error with the user's comment or formatting)
                        if error_reply: item.reply(error.message)
                        item.mark_read()
                        continue
                    except Exception as e: # however, if this happens, the bot gives a generic reply
                        if error_reply: item.reply(GenericErrorMessage)
                        item.mark_read()

                        for user in bot_managers: # message the users in bot_managers (above)
                            try: reddit.redditor(user).message('DiceBot error!', f'Parse error: {e}')
                            except Exception as e: print(e); continue
                        continue # continue to the next comment found

                interpreter = Interpreter(rolls)
                result, error = interpreter.translate()
                if error:
                    print(item.id + ': ' + error.as_string())
                    try: # these errors also shouldn't happen most of the time, so we'll send another generic reply
                        if error_reply: item.reply(error.message)
                        item.mark_read()
                        continue
                    except Exception as e: # again, send a message to bot_managers
                        if error_reply: item.reply(GenericErrorMessage)
                        item.mark_read()

                        for user in bot_managers:
                            try: reddit.redditor(user).message('DiceBot error!', f'Interpreter error: {error.as_string()}')
                            except Exception as e: print(e); continue
                        continue

                item.mark_read() # Mark the comment as read so it won't be read again

                # Construct and send the reply to the comment
                output = make_reply()
                item.reply(output)

                # Print results to the console
                print(f"{item.author} rolled: {result}")

            else: item.mark_read() # Mark non-roll messages as read just to get them out of the way

    except Exception as e: # This should only happen when the bot encounters a server error while trying to check the inbox
        s = retry_wait_time # It'll wait a specified amount of time before trying again to avoid spamming the console with errors
        while s > 0:
            s -= 1
            print(f"ERROR: {e} -- Trying again in {s} seconds...", end="\r")
            time.sleep(1)
        continue
