#!/usr/bin/env python
# coding=utf-8

from copy import deepcopy

CODEC = 'utf-8'

# fileName = "/Users/Qingwei/Documents/workspace/Clion/OJSolutions/jobdu/ex_MaxSumIn2DCycleArray.cpp"
# fileName = "/Users/Qingwei/Downloads/MaxSumIn2DCycleMatrix.java"
fileName = "../in.txt"
file_handle = open(fileName, 'r')
content_in_rows = file_handle.readlines()
new_content_in_rows = []

flag_comment = False
for row in content_in_rows:
    urow = row.decode(CODEC).strip(' ')
    if urow is None or urow == u'' or urow == u'\n' or urow.startswith(u"//"):
        pass
    else:
        if urow.startswith(u"/*"):
            if not urow.endswith(u'*/'):
                flag_comment = True
            else:
                pass
        else:
            if flag_comment:
                trow = deepcopy(urow).strip()
                if trow.endswith(u"*/"):
                    flag_comment = False
            else:
                new_content_in_rows.append(urow.encode(CODEC))

file_handle.close()


# write back
file_handle = open(fileName, 'w')
file_handle.writelines(new_content_in_rows)
file_handle.close()
