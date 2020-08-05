#!/usr/bin/env python
# coding=utf-8
'去掉每行开头的数字与逗号，用uniocde的等式，支持中文，GBK编码'

import os

CODEC = 'GBK'
fileName = raw_input('Please input the file name: ')
file_handle = open(fileName, 'r')
content_in_rows = file_handle.readlines()
new_content_in_rows = []

for row in content_in_rows:
    row = row.decode(CODEC).lstrip()
    # row = row.lstrip()
    index = 0

    for char in row:
        if char.isdigit() or char == u',' or char == u'，':
            index += 1
        else:
            break

    new_content_in_rows.append(row[index:].lstrip().encode(CODEC))

file_handle.close()


#write back
file_handle = open(fileName, 'w')
file_handle.writelines(new_content_in_rows)
file_handle.close()
