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

	# Adds characters to command until space, unless quotes are around input. Backslashes stop fn of following char
	for i in range(len(inp)):
		current = inp[i]
		if current == "\\":
			backslash = True
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

	return(tokens)


# Parses and executes tokens
def parse(tokens):
	# state machine (ints)
	# global var next state (0 = expecting command)
	# parser. get me next token. if statement, if state is expecting command do x
	# ? stack = []
	# for element in tokens:
	pass

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
			tokenize(commands)

if __name__ == "__main__":
	main()


