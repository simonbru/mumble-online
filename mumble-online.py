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
	return u'\x1b[{}m{}\x1b[0m'.format(color_id, string)


def format_chan(subtree):
	yield subtree.c.name
	for user in subtree.users:
		yield u'├─ ' + format_user(user)
	for child in subtree.children:
		child_lines = list(format_chan(child))
		yield u'├─ ' + child_lines[0].decode('utf8')
		for line in child_lines[1:]:
			yield u'│  ' + line


def format_user(user):
	status = u''
	if user.selfDeaf:
		status = u' [deaf]'
	elif user.selfMute:
		status = u' [mute]'
	return u'{}{}'.format(
		color(92, user.name.decode('utf8')),
		color(91, status),
	)


raw_fortune = check_output('/usr/games/fortune -s -n 50 -o'.split(' '))
fortune = ', '.join(
	line.strip() for line in raw_fortune.split('\n') if line.strip()
)

while True:
	server = mice.s
	tree = server.getTree()
	os.system('clear')
	print(u'Rababou - {:%H:%M:%S} ~ {}\n'.format(
		datetime.now(), fortune
	))
	print(*format_chan(tree), sep='\n')
	time.sleep(5)
