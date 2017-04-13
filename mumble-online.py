#!/usr/bin/env python3
from __future__ import print_function
import time, mice, sys

while True:
	time.sleep(1)
	print('\r', [u.name for u in mice.m.getServer(1).getUsers().values()], end='')
	sys.stdout.flush()
