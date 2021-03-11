import os
import subprocess
import re

'''
SEAshell
By Andromeda Kepecs
Date Created: March 10, 2021
Last Modified: 3/10/2021
'''

# Colored text
class col:
	BAD = '\033[91m'	# Warnings, exceptions, etc.
	IN = '\u001b[37m'	# User input
	OUT = '\u001b[32m'	# Shell output
	PROMPT = '\033[96m'	# Shell prompt

# Creates tokens from user input, accounting for quotes and backslashes
def tokenize(commands):

	new = commands

	if "\\" in commands:	# Backslash
		new = ""
		for i in range(len(commands)):
			if commands[i] == "\\":
				if commands[i + 1] == '"':
					new += "%"
			else:
				new += commands[i]

	if '"' in new:	# Quotes
		new1 = ""
		quote = False
		for char in new:
			if char == '"':
				if quote == False:
					quote = True
				else:
					quote = False
			if quote == True and char == " ":
				new1 += "$"
			else:
				if char != '"':
					new1 += char
		commands = new1


	temp = commands.split(" ")
	temp1 = [item.replace('$', ' ') for item in temp]
	tokens = [item.replace('%', '"') for item in temp1]

# Parses and executes
def execute_commands(commands):
	command_tokens = tokenize(commands)
	print(command_tokens)

def expand(wildcard):
	pass

def pwd():
	return str(os.getcwd())

def help():
	print(col.OUT + "hi")

# Main
print(col.OUT + "Welcome to the Swaggy Elementary Andromeda shell")
def main():
	while True:
		commands = input(col.PROMPT + "SEAshell:" + str(os.path.basename(os.getcwd())) + " " + os.getlogin() + "$ " + col.IN)
		if commands == "exit":
			print(col.OUT + "Terminated")
			break
		elif commands == "help":
			help()
		else:
			execute_commands(commands)

if __name__ == "__main__":
	main()

