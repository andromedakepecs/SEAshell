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
	IN = '\u001b[37m'	# User input and files (white)
	OUT = '\u001b[32m'	# Shell output (green)
	PROMPT = '\033[96m'	# Shell prompt (cyan)
	BOLD = '\u001b[35m'	# Bold (magenta)

# Creates tokens from user input accounting for quotes and backslashes
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
# TODO: wild cards, flags 
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
		elif inp == "ls":	# List files
			ls()
		else:
			print(col.BAD + "Invalid command, type \"help\" for list of available commands")
	else:
		if tokens[0] == "cd":	#Change CWD
			cd(tokens[1])
		elif tokens[0] == "echo":	# Echo input
			out = ""
			for element in tokens:
				if element != "echo":
					out += element + ' '
			print(out)
		elif "|" in tokens:	# Piping
			pipe(tokens)
		else:
			print(col.BAD + "Invalid command, type \"help\" for list of available commands")

# TODO
def expand(wildcard):
	pass

# TODO probably gonna get really messy. decide how execute commands and pipe are gonna tie together since interconnected
def pipe(tokens):
	f_in = os.dup(0)
	f_out = os.dup(1)
	fdin = os.dup(f_in)
	for cmd in 



# Print current working directory
def pwd():
	print(col.OUT + str(os.getcwd()))

# Returns currently running processes TODO: formatting
def jobs():
	output = subprocess.Popen(['ps', '-U', '0'], stdout=subprocess.PIPE).communicate()[0]
	return output

# Lists files in current directory TODO: flags
def ls():
	output = str(subprocess.call("ls"))
	return output[:-1]	# Hides exit status

# Changes working directory TODO: add shortcuts
def cd(path):
	if path == "home":
		home = os.path.expanduser('~')
		os.chdir(home)
	else:
		try:
			os.chdir(path)
		except OSError:
			print(col.BAD + "Unable to change current working directory")

# TODO
def help():
	print(col.OUT + "help")

# Indicate superuser
def prompt():
	if os.geteuid() == 0:
		prompt = "# "
	else:
		prompt = "$ "
	return prompt

# Main
def main():
	print(col.BOLD + "Welcome to the Swaggy Elementary Andromeda shell")
	while True:
		commands = input(col.PROMPT + "SEAshell:" + str(os.path.basename(os.getcwd())) + " " + os.getlogin() + prompt() + col.IN)
		if commands == "exit":
			print(col.OUT + "Terminated")
			break
		elif commands == "help":
			help()
		else:
			execute_commands(commands)

if __name__ == "__main__":
	main()

