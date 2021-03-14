import os
import subprocess
import sys


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

# Parses and executes tokens. Does not support semicolons
# TODO $(x)
def parse(tokens):
	expecting = "command"	# Shell always begins by expecting command
	stack = []	
	for i in range(len(tokens)):
		element = tokens[i]
		# TODO other special cases
		if expecting == "command":	# Command parsing segment
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
				break
			else: 	# Shell builtins
				x_ok1 = os.access("/bin/" + element, os.X_OK)
				x_ok2 = os.access("/usr/bin/" + element, os.X_OK)
				if x_ok1 or x_ok2:	# Checks if executable
					stack.append(element)
					expecting = "argument"
				else:
					print(Color.BAD + "Command not found. Type \"help\" for list of commands.")

		if expecting == "argument":	# Parses other arguments, including wildcards
			# if there is no next token, execute stack
			# if next token is operator, expecting = operator. 
			# also execute commands on stack and get ready to do something with output
			pass
		if expecting == "operator":	# Dealing with operators
			# after doing certain functions, expecting = target
			pass
		if expecting == "target":	# Dealing with operator target files
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
			tokens = tokenize(commands)
			parse(tokens)

if __name__ == "__main__":
	main()


