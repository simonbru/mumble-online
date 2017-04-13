#!/usr/bin/env python2
# -*- coding: utf-8
from __future__ import print_function

import itertools
import os
import re
import sys
import time
from datetime import datetime
from subprocess import check_output

import mice


def color(color_id, string):
	return u'\x1b[{}m{}\x1b[0m'.format(color_id, string)


def clear():
	print('\x1b[2J\x1b[H', end='')


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


def get_fortune():
	raw_fortune = check_output(
		'/usr/games/fortune -s -n 50 -o'.split(' ')
	)
	lines = []
	for line in raw_fortune.split('\n'):
		line = line.strip()
		if not line:
			continue
		if not re.search('[:,.!?]$', line):
			line += ','
		lines.append(line)
	return u' '.join(lines)


def render_screen(tree):
	tree.c.name = u'Rababou'
	yield u'{:%H:%M:%S} ~ {}\n'.format(datetime.now(), fortune)
	for line in format_chan(tree):
		yield line


fortune = get_fortune()
server = mice.s
old_lines = []
skip_count = 0
while True:
	tree = server.getTree()
	lines = list(render_screen(tree))
	if skip_count < 30 and old_lines[1:] == lines[1:]:
		skip_count += 1
	else:
		print('\x1b[2J\x1b[H', end='')
		print(*lines, sep='\n')
		skip_count = 0
		old_lines = lines
	time.sleep(1)
