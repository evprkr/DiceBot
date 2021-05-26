import re
from random import randint
from errors import *

###############################################################################################################

# TOKENS
class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

T_OPEN =    'OPEN'      # Open bracket [
T_CLOSE =   'CLOSE'     # Close bracket ]
T_DIE =     'DIE'       # Die indicator d/D
T_LABEL =   'LABEL'     # Roll label (Damage, To Hit, etc)
T_NUMBER =  'NUMBER'    # Integer 0-9
T_PLUS =    'PLUS'      # Plus +
T_MINUS =   'MINUS'     # Minus -
T_END =     'END'       # End of tokens

###############################################################################################################

# LEXER
NUMBERS = '0123456789'
LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.index = -1
        self.error = None

    def advance(self):
        self.index += 1
        self.char = self.text[self.index] if self.index < len(self.text) else None

    def peek_char(self, n):
        if self.index < len(self.text):
            return self.text[self.index+n]

    def extract_commands(self):
        cmd_list = re.findall('\[.*?\]', self.text)
        if len(cmd_list) == 0: return None
        return cmd_list

    def tokenize(self):
        tokens = []

        # CHECK COMMENT TEXT FOR COMMANDS
        cmd_list = self.extract_commands()
        if cmd_list == None: return None, NoCommandError('No command found in comment')
        cmd_string = str(cmd_list)
        self.text = cmd_string.strip('[').strip(']')
        #print(f"COMMANDS: {self.text}")

        self.advance()

        # TOKENIZE COMMANDS
        while self.char != None:
            if self.char in NUMBERS: tokens.append(self.lex_number())
            elif self.char in LETTERS: tokens.append(self.lex_string())
            elif self.char == '[': tokens.append(Token(T_OPEN)); self.advance()
            elif self.char == ']': tokens.append(Token(T_CLOSE)); self.advance()
            elif self.char == '+': tokens.append(Token(T_PLUS)); self.advance()
            elif self.char == '-': tokens.append(Token(T_MINUS)); self.advance()
            else: self.advance()

        return tokens, None

    # CREATE NUMBER TOKENS
    def lex_number(self):
        number = ''

        while self.char != None and self.char in NUMBERS:
            number += self.char
            self.advance()

        return Token(T_NUMBER, number)

    # CREATE LABEL TOKENS
    def lex_string(self):
        string = ''

        while self.char != None and self.char in LETTERS + ' ':
            string += self.char
            self.advance()

        # Return a DIE token if the entire string is just 'd', otherwise it's just a LABEL token
        if string.lower() == 'd': return Token(T_DIE)
        return Token(T_LABEL, string)

###############################################################################################################

# PARSER NODES
class RollNode:
    def __init__(self, die, modifier, label, roll_number):
        self.die = die
        self.modifier = modifier
        self.label = label
        self.roll_number = roll_number

    def __repr__(self):
        if self.modifier != None:
            if self.label != None:
                return f"Roll #{self.roll_number}: {self.die}{self.modifier} {self.label}" # die + modifier + label
            return f"Roll #{self.roll_number}: {self.die}{self.modifier}" # die + modifier, no label

        if self.label != None: return f"Roll #{self.roll_number}: {self.die} {self.label}" # die + label, no modifier

        return f"Roll #{self.roll_number}: {self.die}" # only die, no modifier or label

class DieNode:
    def __init__(self, count, size):
        self.count = count
        self.size = size

    def __repr__(self):
        return f"{self.count.value}d{self.size.value}"

class ModifierNode:
    def __init__(self, operator, number):
        self.operator = operator
        self.number = number

    def __repr__(self):
        return f"{self.operator}{self.number}"

class LabelNode:
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return self.label

class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value

# PARSER CLASS
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.roll_number = 1
        self.error = None
        self.advance()

    def advance(self):
        self.index += 1
        self.token = self.tokens[self.index] if self.index < len(self.tokens) else None

    def parse(self):
        rolls = []

        while self.token != None and self.error == None:
            command = self.parse_roll()
            if command == None: break
            if self.error: return None, self.error
            rolls.append(command)
            self.roll_number += 1
            self.advance()

        # If parsing finishes but we haven't reached the end yet, this should never happen
        if not self.error and self.index < len(self.tokens):
            self.error = Error("[!] CRITICAL PARSE ERROR [!]")
            return None, self.error

        return rolls, None

    def parse_roll(self):
        while self.token != None and self.token.type in (T_OPEN, T_CLOSE): self.advance()
        if self.token == None: return

        # PARSE DIE (REQUIRED)
        if self.token.type in (T_NUMBER, T_DIE):
            die = self.parse_die()
            if self.error:
                if not self.error: self.error = Error("Invalid die node")
                return self.error
            self.advance()
        else:
            print(self.token)
            self.error = Error("Expected NUMBER or DIE token in parse_roll()")
            return self.error

        # PARSE MODIFIER (OPTIONAL)
        if self.token.type in (T_PLUS, T_MINUS):
            modifier = self.parse_modifier()
            if self.error:
                if not self.error: self.error = Error("Invalid modifier node")
                return self.error
            self.advance()
        else: modifier = None

        # PARSE LABEL (OPTIONAL)
        if self.token.type == T_LABEL:
            label = self.parse_label()
            if self.error:
                if not self.error: self.error = Error("Invalid label node")
                return self.error
        else: label = None

        # RETURN COMPLETED ROLL NODE
        return RollNode(die, modifier, label, self.roll_number)

    def parse_die(self):
        count = 1

        if self.token.type == T_NUMBER:
            count = NumberNode(self.token.value)
            if int(count.value) == 0:
                self.error = Error("Zero is not allowed in die count or die size")
                return self.error
            self.advance()

        if self.token.type == T_DIE:
            self.advance()
            if self.token.type == T_NUMBER: size = NumberNode(self.token.value)
            else: self.error = Error("Expected NUMBER token in parse_die()")
            size = NumberNode(int(self.token.value))

        return DieNode(count, size)

    def parse_modifier(self):
        operator = '+' if self.token.type == T_PLUS else '-'
        self.advance()

        if self.token.type == T_NUMBER: number = NumberNode(self.token.value)
        else: self.error = Error("Expected NUMBER token in parse_modifier()")

        return ModifierNode(operator, number)

    def parse_label(self):
        label = self.token.value
        return LabelNode(label)

    def parse_number(self):
        number = str(self.token.value)
        return NumberNode(number)

###############################################################################################################

# NODE VALUES
class Number:
    def __init__(self, value):
        self.value = value

    def math_add(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value), None
        else: return None, Error("Illegal operation")

    def math_sub(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value), None
        else: return None, Error("Illegal operation")

    def __repr__(self):
        return str(self.value)

class Modifier:
    def __init__(self, operator, number):
        self.operator = operator
        self.number = number

    def __repr__(self):
        return f"{self.operator}{self.number}"

class Label:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return (str(self.value))

# INTERPRETER CLASS
class Interpreter:
    def __init__(self, rolls):
        self.rolls = rolls
        self.error = None

    def translate(self):
        output = []
        for roll in self.rolls:
            result = self.roll_die(roll.die)

            # If the roll has a modifier, apply it
            if roll.modifier != None:
                result = self.apply_modifier(result, roll.modifier)

            # If the roll has a label, attach it
            if roll.label != None:
                result = f"{result} {roll.label}"

            output.append(result)

        return output, None

    def roll_die(self, die):
        results = []
        roll_total = 0
        try: count = int(die.count.value)
        except: count = 1
        size = int(die.size.value)

        # Roll the specified number of dice
        for i in range(count):
            roll = randint(1, size)
            results.append(roll)

        # Add each roll to the total
        for i in results:
            roll_total += i

        return roll_total

    def apply_modifier(self, result, modifier):
        operator = modifier.operator
        number = int(modifier.number.value)

        if operator == '+': return result + number
        return result - number
