import os
import subprocess

'''
SEAshell
By Andromeda Kepecs
Date Created: March 10, 2021
Last Modified: 3/10/2021
'''

# Colored text
class col:
	BAD = '\033[91m'	# Warnings, exceptions, etc. (red)
	IN = '\u001b[37m'	# User input (white)
	OUT = '\u001b[32m'	# Shell output (green)
	PROMPT = '\033[96m'	# Shell prompt (cyan)
	BOLD = '\u001b[35m'	# Bold (magenta)

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

	return tokens

# Parses and executes commands
# TODO: wild cards, flags maybe
def execute_commands(commands):
	tokens = tokenize(commands)
	if len(tokens) == 1:
		inp = tokens[0]
		if inp == "pwd":	# Working directory filepath
			pwd()
		elif inp == "jobs":	# Running processes
			print(col.OUT + str(jobs()))
		elif inp == "cd":	# Home directory
			cd("home")
		elif inp == "ls":
			ls()
	elif len(tokens) == 2:
		if tokens[0] == "cd":
			cd(tokens[1])
	
# TODO
def expand(wildcard):
	pass

# Print current working directory
def pwd():
	print(col.OUT + str(os.getcwd()))

# Returns currently running processes
def jobs():
	output = subprocess.Popen(['ps', '-U', '0'], stdout=subprocess.PIPE).communicate()[0]
	return output

# Lists files in current directory
def ls():
	output = str(subprocess.call("ls"))
	return output[:-1]	# Hides exit status

# TODO
def cd(path):
	if path == "home":
		home = os.path.expanduser('~')
		os.chdir(home)
		


# TODO
def help():
	print(col.OUT + "help")

# Main
def main():
	print(col.BOLD + "Welcome to the Swaggy Elementary Andromeda shell")
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

