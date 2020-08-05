#!/usr/bin/env python
# coding=utf-8
"""delete the arrow > and space in the front of rows in the file inputted."""

import os

# fileName = raw_input('Please input the file name: ')
# file_handle = open(fileName, 'r')
file_handle = open('../in.txt', 'r')
content_in_rows = file_handle.readlines()
new_content_in_rows = []

for row in content_in_rows:
    row = row.lstrip()
    index = 0
    for char in row:
        if char == '>':
            index += 1
        else:
            break

    new_content_in_rows.append(row[index:].lstrip())

file_handle.close()


# write back
# file_handle = open(fileName, 'w')
file_handle = open("out.txt", 'w')
file_handle.writelines(new_content_in_rows)
file_handle.close()
