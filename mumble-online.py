#!/usr/bin/env python2
# -*- coding: utf-8
from __future__ import print_function

import os
import sys
import time
from datetime import datetime

import mice


while True:
	server = mice.m.getServer(1)
	channels = server.getChannels()
	users = server.getUsers().values()
	os.system('clear')
	print('Rababou - {:%H:%M:%S}'.format(datetime.now()))
	if not users:
		print(u"No one here ¯\_(ツ)_/¯")
	for user in sorted(users, key=lambda u: u.channel):
		status = ''
		if user.selfDeaf:
			status = ' [deaf]'
		elif user.selfMute:
			status = ' [mute]'
		chan = channels[user.channel].name
		print('{}{} | {}'.format(user.name, status, chan))
	time.sleep(5)
