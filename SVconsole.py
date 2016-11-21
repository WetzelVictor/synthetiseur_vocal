# -*- coding: utf-8 -*-
# File SVconsole.py
"""
Projet: Vocal controlled synthL
date: octobre 2016
UPMC, Master SdI, acoustique
@authors: lauraparra & victorwetzel
"""

class Console:
	"""class: Console 
	Permet de demander des commandes à l'utilisateur.
	Dans le cadre du projet "synthetiseur vocal", elle 
	permet d'arrêter tous les threads du programme
	proprement. 
	"""
	def __init__(self):
		self.userInput = ''
		self.start = False
		self.stop  = False


	def ask(self):
		rawInput = raw_input('Enter a command:  ')
		

		if rawInput == 'help':
			self.help()
			self.ask()
		elif rawInput == 'start':
			self.start = True
			self.pause = False
			print('Starting...')
			self.ask()
		elif rawInput == 'stop':
			self.stop = True
			return
		else:
			print('I did not understand...\n')
			self.ask()
		
		
		return

	def askFirst(self):
		cond_while = True
		rawInput = ''
		while cond_while:	
			rawInput = raw_input('Should we start? [y/n] : ')
			if rawInput == 'y':
				self.start = True
				cond_while = False
			elif rawInput == 'n':
				self.stop = True
				exit()
			else :
				print('I did not understand...\n')
		return


	def help(self):
		print('Commands : start, stop \nGuess what is does... ;)  )\n')
