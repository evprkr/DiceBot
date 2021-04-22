# This error system is pretty basic right now. I might flesh it out and make it more robust later on.
# Any errors that happen in lexing/parsing will be sent to me for review, and the person who requested the roll
# will just receive a generic "something went wrong" message.

# ERROR RESPONSE MESSAGES (These can be modified, but can't contain double quotes or backslashes)
# These messages are sent as replies or DMs (or both) depending on the settings in 'dicebot.py'
NoCommandMessage = "I didn't find any commands in your comment, enter commands like so: [2d8+4 damage], commands can be anywhere in your comment and you can have as many as you want. (Labels like 'damage' or 'to hit' are optional)"

# ERROR CLASS
class Error:
    def __init__(self, details, message=None):
        self.details = details
        self.message = message

    def as_string(self):
        error_msg = f"ERROR: {self.details}"
        return error_msg

# ERROR TYPES
class NoCommandError(Error):
    def __init__(self, details):
        super().__init__(details, NoCommandMessage)
