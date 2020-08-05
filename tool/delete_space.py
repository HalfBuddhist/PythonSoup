#!/usr/bin/env python
# coding=utf-8

s = \
    """
68. Text Justification
    """
ans = ''
is_first = True
for c in s:
    if c in '- ':  # neglect and set first flag
        is_first = True
    else:
        # for replace
        if c in '.':
            c = '_'
        # upper the letter
        if is_first and c.isalpha():
            c = c.upper()
            is_first = False
        ans += c

print(ans)