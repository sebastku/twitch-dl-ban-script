#!/usr/bin/env python3
import os
import os.path
import sys
import platform
import jellyfish
import irc.bot

class BanBot(irc.bot.SingleServerIRCBot):
	def __init__(self, username, token, channel, dl_phrases, dl_users, 
	directorySeperator):
		self.username = username
		self.token = token
		self.channel = channel
		self.dl_phrases = dl_phrases
		self.dl_users = dl_users
		self.directorySeperator = directorySeperator
		server = 'irc.chat.twitch.tv'
		port = 6667
		print('Connecting to the Twitch servers as ' + username)
		irc.bot.SingleServerIRCBot.__init__(self, 
		[(server, port, token)], username, username)

	def on_welcome(self, connection, event):
		print('Joining ' + self.channel)
		connection.join('#' + self.channel)
		connection.privmsg('#' + event.target, 
		'WARNING! A script that automatically bans ' +
		'potential disturbers is now running!')
		connection.privmsg('#' + event.target, 
		'If you get banned for no reason, please message me. ' +
		'I will unban and whitelist you if you are no bot.')

	def on_pubmsg(self, connection, event):
		message = event.arguments[0]
		autor = self.split_username(event.source)
		# Check whether the autor is whitelisted
		if self.entry_on_list(autor, self.channel + 
		self.directorySeperator + 'whitelist.txt'):
			return
		# Check whether the autor has a sufficient distance 
		# to the blacklist for usernames
		if self.match_blacklist(autor, self.channel + 
		self.directorySeperator + 'blacklist-users.txt', self.dl_users):
			self.ban(connection, channel, autor)
			return
		# Check whether the message has a sufficient distance 
		#to the blacklists for phrases
		i = 1
		while (os.path.isfile(self.channel + self.directorySeperator + 
		'blacklist-phrase-' + str(i) + '.txt')):
			if self.match_blacklist(message, self.channel + 
			self.directorySeperator + 'blacklist-phrase-' + 
			str(i) + '.txt', self.dl_phrases):
				self.ban(connection, channel, autor)
				return
			i = i+1

	def entry_on_list(self, match, filename):
		file = open(filename)
		content = file.read().splitlines()
		file.close()
		for entry in content:
			if match == entry.lower():
				return True
		return False

	def match_blacklist(self, match, filename, dl_distance):
		file = open(filename)
		content = file.read().splitlines()
		file.close()
		for entry in content:
			if jellyfish.damerau_levenshtein_distance(
			entry.lower(), match.lower()) <= dl_distance:
				return True
		return False

	def ban(self, connection, channel, user):
		connection.privmsg('#' + channel, '/ban ' + user)

	@staticmethod
	def split_username(user_id):
		return user_id.split('!', 1)[0]



# Check for config.py
if not os.path.isfile('config.py'):
	sys.exit('Please create a valid config.py as described in ' +
	'README.md')
import config as cfg

# Parse command line arguments
if len(sys.argv) == 1:
	sys.exit('Usage: banscript.py <CHANNEL NAME> [OPTIONS]')
elif len(sys.argv) == 2:
	channel = sys.argv[1].lower()
else:
	channel = sys.argv[1].lower()
	# TODO: Implement command line options
	sys.exit('To be implemented...')

# Determine the platform the script is running on
if platform.system() == 'Windows':
	directorySeperator = '\\'
else:
	directorySeperator = '/'

# Check whether a directory for the channel exists 
if not os.path.isdir(channel):
	os.mkdir(channel)
	whitelist = open(channel + directorySeperator + 'whitelist.txt','a')
	whitelist.write(channel + '\n')
	if not cfg.username.lower() == channel:
		whitelist.write(cfg.username + '\n')
	whitelist.close()
	blacklistUsers = open(channel + directorySeperator + 
	'blacklist-users.txt', 'a')
	blacklistUsers.close()
	blacklistPhrase = open(channel + directorySeperator + 
	'blacklist-phrase-1.txt', 'a')
	blacklistPhrase.close()
	sys.exit('Please set up your blacklists first before running' +
	' the script')

# Start the bot
bot = BanBot(cfg.username.lower(), cfg.token, channel, cfg.dl_phrases, 
cfg.dl_users, directorySeperator)
bot.start()
