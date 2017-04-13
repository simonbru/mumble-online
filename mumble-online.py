#!/usr/bin/env python2
# -*- coding: utf-8
from __future__ import print_function

import itertools
import os
import sys
import time
from datetime import datetime
from subprocess import check_output

import mice


def color(color_id, string):
	return '\x1b[{}m{}\x1b[0m'.format(color_id, string)


def group_by(iterable, key):
	data = sorted(iterable, key=key)
	return dict(
		(key, list(group))
		for key, group in itertools.groupby(data, key)
	)


def format_chan(channel, channels_by_parent, users_by_chan):
	yield channel.name
	for user in users_by_chan.get(channel.id, []):
		yield u'├─ ' + format_user(user)
	for child_chan in channels_by_parent.get(channel.id, []):
		child_lines = list(format_chan(
			child_chan, channels_by_parent, users_by_chan
		))
		yield u'├─ ' + child_lines[0].decode('utf8')
		for line in child_lines[1:]:
			yield u'│  ' + line


def format_user(user):
	status = ''
	if user.selfDeaf:
		status = ' [deaf]'
	elif user.selfMute:
		status = ' [mute]'
	return '{}{}'.format(
		color(92, user.name.decode('utf8')),
		color(91, status),
	)


raw_fortune = check_output('/usr/games/fortune -s -n 50 -o'.split(' '))
fortune = ', '.join(
	line.strip() for line in raw_fortune.split('\n') if line.strip()
)

while True:
	server = mice.m.getServer(1)
	channels = server.getChannels()
	users = server.getUsers().values()
	os.system('clear')
	print('Rababou - {:%H:%M:%S} ~ {}'.format(datetime.now(), fortune))
	print()
	channels_by_parent = group_by(
		channels.values(), key=lambda c: c.parent
	)
	users_by_chan = group_by(users, key=lambda u: u.channel)
	print(
		*format_chan(channels[0], channels_by_parent, users_by_chan),
		sep='\n'
	)
	time.sleep(5)
