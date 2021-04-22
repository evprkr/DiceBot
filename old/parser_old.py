import re
from errors import *

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
            elif self.char == '[': tokens.append(T_OPEN); self.advance()
            elif self.char == ']': tokens.append(T_CLOSE); self.advance()
            elif self.char == '+': tokens.append(T_PLUS); self.advance()
            elif self.char == '-': tokens.append(T_MINUS); self.advance()
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

# PARSER NODES
class RollNode:
    def __init__(self, die, label):
        self.die = die
        self.label = label

    def __repr__(self):
        return f"ROLL: {self.die} {self.label}"

class DieNode:
    def __init__(self, die_count, die_size, die_mod=None, mod_amount=None):
        self.die_count = die_count
        self.die_size = die_size
        self.die_mod = die_mod
        self.mod_amount = mod_amount

    def __repr__(self):
        if self.die_mod != None: return f"{self.die_count}d{self.die_size}{self.die_mod}{self.mod_amount}"
        return f"{self.die_count}d{self.die_size}"

class LabelNode:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return self.text

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

        # If parsing finishes but we haven't reached the end yet, throw an error
        if not self.error and self.index < len(self.tokens):
            self.error = "CRITICAL PARSE ERROR"
            return None, self.error

        return rolls, None

    def parse_roll(self):
        die = None
        label = None

        while self.token in (T_OPEN, T_CLOSE): self.advance()
        if self.token == None: return

        if self.token.type in (T_DIE, T_NUMBER):
            die = self.parse_die()
            if self.error:
                if not self.error: self.error = Error("Invalid Die")
                return self.error

        if self.token.type == T_LABEL:
            label = LabelNode(self.token.value)
            if self.error:
                if not self.error: self.error = Error("Invalid label")
                return self.error
            self.advance()

        if die != None:
            return RollNode(die, label)

        if not self.error: self.error = Error("Invalid roll")
        return self.error

    def parse_die(self):
        die_count = 1 # Default number of dice to roll if none is specified

        if self.token.type == T_NUMBER:
            die_size = self.token.value
            self.advance()

        if self.token.type == T_DIE:
            die_count = 1
            self.advance()

        if self.token.type == T_NUMBER:
            die_size = self.token.value
            self.advance()

        if self.token in (T_PLUS, T_MINUS):
            die_mod = self.token
            self.advance()
            if self.token.type == T_NUMBER:
                mod_amount = self.token.value
                self.advance()
            else:
                self.error = Error("Invalid modifier")
                return self.error

        return DieNode(die_count, die_size, die_mod, mod_amount)

# VALUES
class Number:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

# INTERPRETER CLASS
class Interpeter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_DieNode(self, node):
        pass

    def visit_RollNode(self, node):
        pass

    def visit_LabelNode(self, node):
        pass
