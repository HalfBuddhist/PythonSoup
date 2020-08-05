#!/usr/bin/env python
# coding=utf-8
import os

file = open("files.txt", "r")
for line in file:
    name = line.strip()
    if os.path.isfile(name):
        pass
        # print name, 'true'
    else:
        print name, 'false'
file.close()
