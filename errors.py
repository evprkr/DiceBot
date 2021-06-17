# This error system is pretty basic right now. I might flesh it out and make it more robust later on.
# any errors with commands or formatting will be explained to the user who sent them, and printed to the console
# more serious errors generate a generic reply for the user and then sends a PM to the users in bot_managers in dicebot.py

# ERROR RESPONSE MESSAGES (These can be modified, but can't contain double quotes or backslashes)
# These messages are sent as replies or DMs (or both) depending on the settings in 'dicebot.py'
GenericErrorMessage = "Something went wrong... I'm not sure what, but I've notified the developer. Sorry!"
InvalidCommandMessage = "The meaning of your command eludes me... Please try again."
NoCommandMessage = "I didn't find any commands in your comment, enter commands like so: [2d8+4 damage] -- commands can be anywhere in your comment and you can have as many as you want. \n\n(Labels like 'damage' or 'to hit' or 'because I said so' are optional)"
ZeroRollMessage = "I can't roll zero dice! (Or a zero-sided die either, I'm not really sure how that would work.)"

# MAIN ERROR CLASS
class Error:
    def __init__(self, details, message=None):
        self.details = details
        self.message = message

    def as_string(self):
        error_msg = f"ERROR: {self.details}"
        return error_msg

# ERROR TYPES
class InvalidCommandError(Error):
    def __init__(self, details, message=InvalidCommandMessage):
        super().__init__(details, message)

class NoCommandError(Error):
    def __init__(self, details, message=NoCommandMessage):
        super().__init__(details, message)

class ZeroRollError(Error):
    def __init__(self, details, message=ZeroRollMessage):
        super().__init__(details, message)
