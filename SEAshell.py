import os
import subprocess

'''
SEAshell
Author: Andromeda Kepecs
'''

# Colored text
class Color:
	BAD = '\033[91m'	# Warnings, exceptions, etc. (red)
	IN = '\u001b[37m'	# User input and files (white)
	OUT = '\u001b[32m'	# Shell output (green)
	PROMPT = '\033[96m'	# Shell prompt (cyan)
	BOLD = '\u001b[35m'	# Bold (magenta)

# Changes working directory TODO: add shortcuts 
def cd(path):
	if path == "home":
		home = os.path.expanduser('~')	# Universal home directory
		os.chdir(home)
	elif path == "-":
		# TODO switch to previous directory
		pass
	else:
		try:
			os.chdir(path)
		except OSError:
			print(Color.BAD + "Unable to change current working directory")

# Turns input into list of tokens
def tokenize(inp):
	if inp[-1] != " ":	# Caters to appending commands based on spaces
		inp += " "

	cmd = ""
	quotes = False
	backslash = False
	tokens = []

	# Adds characters to command until space, unless quotes are around input. 
	# Backslashes stop fn of following char, currently only supports quotes. TODO wild cards
	for i in range(len(inp)):
		current = inp[i]
		if current == "\\":
			if not backslash:
				backslash = True
			else:
				backslash = False
		if current == '"':
			if not backslash:
				if not quotes:
					quotes = True
				else:
					quotes = False
			else:
				cmd += current
				backslash = False
		if current == " ":
			if not quotes:
				tokens.append(cmd)
				cmd = ""
			else:
				cmd += current
		elif current != '"' and not backslash:
			cmd += current

	return tokens

# Parses and executes tokens
# TODO $(x)
# Does not support semicolons
def parse(tokens):
	# state machine (expecting)
	# global var next state (0 = expecting command)
	# parser. get me next token. if statement, if state is expecting command do x
	# ? stack = []

	# Tracks execution state. 
	# 0 = expecting command (first thing) (when expecting command look at if builtin table or look in /bin, userlocal bin home directory etc)
	# need full path to command unless it's a builtin
	# 1 = expecting arguments, . by default processing argument unless see other things. deal with wildcards here
	# 2 = expecting operator, 3 = expecting target


	expecting = "command"	# Shell begins by expecting command
	stack = []	
	for i in range(len(tokens)):
		element = tokens[i]
		if expecting == "command":
			try:
				if element == "echo":	# Echo special case
					new = ""
					for j in range(i + 1, len(tokens)):
						new += tokens[j] + " "
					print(new)
					break
				if element == "cd":	# Change CWD special case
					if len(tokens) == 1:
						cd("home")
					else:
						cd(tokens[i + 1])
				else:
					if os.path.isfile(element) and os.access(element, os.X_OK):	# Checks if executable exists
						stack.append(element)
						expecting = "argument"
			except Exception:
					print(Color.BAD + "Command not found. Type \"help\" for list of commands.")



# Indicate superuser
def prompt():
	if os.geteuid() == 0:
		prompt = "# "
	else:
		prompt = "$ "
	return prompt

# Main
def main():
	print(Color.BOLD + "Welcome to the Swaggy Expiramental Andromeda shell")
	while True:
		commands = input(Color.PROMPT + "SEAshell:" + str(os.path.basename(os.getcwd())) + " " + os.getlogin() + prompt() + Color.IN)
		if commands == "exit":
			print(Color.OUT + "Terminated")
			break
		elif commands == "help":
			help()
		else:
			tokens = tokenize(commands)
			parse(tokens)

if __name__ == "__main__":
	main()


