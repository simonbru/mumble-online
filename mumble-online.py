#!/usr/bin/env python3

import itertools
import os
import re
import sys
import time
from datetime import datetime
from enum import IntEnum
from subprocess import check_output

import mice3 as mice

from config import HIDE_EMPTY_CHANS, SERVER_NAME, SPECIAL_USERS


class Color(IntEnum):
	"""Terminal color"""
	LIGHT_RED = 91
	LIGHT_GREEN = 92
	LIGHT_BLUE = 94


def colorize(color, string):
	return '\x1b[{}m{}\x1b[0m'.format(color, string)


def clear():
	print('\x1b[2J\x1b[H', end='')


def has_users(subtree):
	return subtree.users or any(
		has_users(tree) for tree in subtree.children
	)


def format_chan(subtree):
	yield subtree.c.name
	for user in subtree.users:
		yield '├─ ' + format_user(user)
	for child in subtree.children:
		if HIDE_EMPTY_CHANS and not has_users(child):
			continue
		child_lines = list(format_chan(child))
		yield '├─ ' + child_lines[0]
		for line in child_lines[1:]:
			yield '│  ' + line


def format_user(user):
	status = ''
	if user.selfDeaf:
		status = ' [deaf]'
	elif user.selfMute:
		status = ' [mute]'
	user_color = Color.LIGHT_GREEN
	if user.name in SPECIAL_USERS or user.userid in SPECIAL_USERS:
		user_color = Color.LIGHT_BLUE
	return '{}{}'.format(
		colorize(user_color, user.name),
		colorize(Color.LIGHT_RED, status),
	)


def get_fortune():
	raw_fortune = check_output(
		'/usr/games/fortune -s -n 50 -o'.split(' ')
	).decode('utf8')
	lines = []
	for line in raw_fortune.split('\n'):
		line = line.strip()
		if not line:
			continue
		if not re.search('[:,.!?]$', line):
			line += ','
		lines.append(line)
	lines[-1] = re.sub(',$', '', lines[-1])
	return ' '.join(lines)


def render_screen(tree):
	yield '{:%H:%M:%S} ~ {}\n'.format(datetime.now(), fortune)
	if HIDE_EMPTY_CHANS and not has_users(tree):
		yield "~ No one is there ~"
	else:
		tree.c.name = SERVER_NAME
		for line in format_chan(tree):
			yield line


fortune = get_fortune()
server = mice.s
old_lines = []
skip_count = 0
while True:
	tree = server.getTree()
	lines = list(render_screen(tree))
	if skip_count < 600 and old_lines[1:] == lines[1:]:
		skip_count += 1
	else:
		print('\x1b[2J\x1b[H', end='')
		print(*lines, sep='\n')
		skip_count = 0
		old_lines = lines
	time.sleep(1)
