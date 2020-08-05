#!/usr/bin/env python
'delete the digit and space in the front of rows in the file inputted.'

import os

fileName = raw_input('Please input the file name: ')
# fileName = "/Users/Qingwei/Documents/workspace/Clion/OJSolutions/jobdu/ex_MaxSumIn2DCycleArray.cpp"
file_handle = open(fileName, 'r')
content_in_rows = file_handle.readlines()
new_content_in_rows = []

for row in content_in_rows:
    row = row.lstrip()
    index = 0

    for char in row:
        if char.isdigit():
            index += 1
        else:
            break

    new_content_in_rows.append(row[index:].lstrip())

file_handle.close()


#write back
file_handle = open(fileName, 'w')
file_handle.writelines(new_content_in_rows)
file_handle.close()
