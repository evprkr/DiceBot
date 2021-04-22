import praw
import re, os, sys, time
import datetime as dt
from random import randint

# Random thoughts and notes

# If the bot tries to reply to someone and is banned from that subreddit, it should PM the person who summoned it and tell
# them that it's banned, but still give them the roll they want. Speaking of, I could make it so you could PM the bot for
# dice rolls as well as mention it by username.

# If someone calls it a good bot, it should award them a point of inspiration for funsies

# I'd also like to add a stat roller function, just 4d6 drop the lowest, called upon with a special command

reddit = praw.Reddit(
	client_id='6J61rYtJNMLj9w',
	client_secret='yam8U2tAXY6X02369hMRyqH9kQNTZQ',
	user_agent='<console:DRB:1.0.0>',
	username='_dice_bot',
	password='Valuecharm1001$')

# Clear the screen before the bot starts doing stuff
os.system('clear')
startTime = str(dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
print('[DiceBot is online at '+startTime+']\n')

while True:
	try:
		for item in reddit.inbox.unread(limit=25):
			# Only find inbox mentions (containing my username)
			if '/u/_dice_bot' in str(item.body) or 'u/_dice_bot' in str(item.body):
					replyTime = str(dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

					# Convert the string to lowercase, then remove the mention
					body = str(item.body).lower()
					body = body.replace('/u/_dice_bot ', '')
					body = body.replace('u/_dice_bot ', '')
				
					# Find if there's a modifier in the comment
					if '+' or '-' in body: split = re.findall(r"[\w']+", body)
				
					# Find the numbers before and after the 'd'
					num = int(split[0].split('d')[0])
					die = int(split[0].split('d')[1])

					total = 0
					
					# Roll the necessary dice and keep track of the total roll
					for i in range(num):
						total += randint(1, die)
		
					# Apply the modifier [REWRITE]
					if '+' in body:
						mod = split[1]
						total += int(mod)
						roll = str(num)+'d'+str(die)+'+'+str(mod)
					elif '-' in body:
						mod = split[1]
						total -= int(mod)
						roll = str(num)+'d'+str(die)+'-'+str(mod)
					else:
						roll = str(num)+'d'+str(die)

					# Reply to the message with the roll results (and apply easter eggs)
					if total == 69: item.reply('You rolled **'+str(total)+'** ('+roll+')\n\nNice.')
					else: item.reply('You rolled **'+str(total)+'** ('+roll+')')

					# Print some stuff because why not
					print('['+str(replyTime)+']/u/'+str(item.author)+' rolled: '+str(total)+' ('+roll+')')

					# Mark the message as read so we don't reply to the same one again, then wait a bit before continuing
					item.mark_read()
					time.sleep(15)
	except Exception as e:
		if 'RATE_LIMIT' in str(e):
			print('Comment limit reached, trying again in two minutes.')
			time.sleep(120)
			continue
		elif '503 HTTP' in str(e):
			print('Reddit is down! Trying again in two minutes.')
			time.sleep(120)
			continue
		else:
			# If something else goes wrong, print the error, reply to the comment, message Nose_Fetish, then carry on
			print('Something went wrong: ' + str(e))
			print(item.body)

			item.reply('I\'m a dumb robot. Please use this syntax to roll: XdY(+/-)Z\n\nIf I failed for some other reason, please tell /u/Nose_Fetish he sucks at Python.')
			item.mark_read()

			# Also PM me with the error so I can fix it if the bot crashes
			reddit.redditor('Nose_Fetish').message('DiceBot Error', 'Exception:\n\n'+str(e))

			# Wait 30 seconds just to be safe, then continue
			time.sleep(30)
			continue
