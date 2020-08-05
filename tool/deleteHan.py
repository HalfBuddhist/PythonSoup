#!/usr/bin/env python
# coding=utf-8

from HanZi import is_chinese_extend

CODEC = 'utf-8'

# fileName = "/Users/Qingwei/Documents/workspace/Clion/OJSolutions/jobdu/ex_MaxSumIn2DCycleArray.cpp"
# fileName = "/Users/Qingwei/Downloads/MaxSumIn2DCycleMatrix.java"
fileName = "../in.txt"
file_handle = open(fileName, 'r')
content_in_rows = file_handle.readlines()
new_content_in_rows = []

for row in content_in_rows:
    new_row = u''
    urow = row.decode(CODEC)
    for uchar in urow:
        if is_chinese_extend(uchar):
            continue
        else:
            new_row += uchar
    new_content_in_rows.append(new_row.encode(CODEC))
file_handle.close()


# write back
file_handle = open(fileName, 'w')
file_handle.writelines(new_content_in_rows)
file_handle.close()
