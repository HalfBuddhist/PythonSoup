#!/usr/bin/env python
# coding=utf-8
"""汉字处理相关"""


def ishan(text):
    # for python 2.x,
    # sample: ishan(u'一') == True, ishan(u'我&&你') == False
    # 常见的 \u4e00-\u9fa5 写太死了，虽说目前而言后面的都是极其罕见的字
    return all(u'\u4e00' <= char <= u'\u9fff' for char in text)


# 判断一个unicode是否是汉字,包含有部首，标点, 平假名 什么的。
def is_chinese_extend(uchar):
    if u'\u2E80' <= uchar <= u'\u9fff':
        return True
    else:
        return False


# 判断一个unicode是否是汉字
def is_chinese(uchar):
    if u'\u4e00' <= uchar <= u'\u9fff':
        return True
    else:
        return False


# 判断一个unicode是否是数字
def is_number(uchar):
    if u'\u0030' <= uchar and uchar <= u'\u0039':
        return True
    else:
        return False


# 判断一个unicode是否是英文字母
def is_alphabet(uchar):
    if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
        return True
    else:
        return False


# 判断是否非汉字，数字和英文字符
def is_other(uchar):
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False

# for version 3.x
# # 判断一个unicode是否是汉字
# def is_chinese(uchar):
#     if '\u4e00' <= uchar<='\u9fff':
#         return True
#     else:
#         return False
#
# # 判断一个unicode是否是数字
# def is_number(uchar):
#     if '\u0030' <= and uchar<='\u0039':
#         return True
#     else:
#         return False
#
# # 判断一个unicode是否是英文字母
# def is_alphabet(uchar):
#     if ('\u0041' <= uchar<='\u005a') or ('\u0061' <= uchar<='\u007a'):
#         return True
#     else:
#         return False
#
# # 判断是否非汉字，数字和英文字符
# def is_other(uchar):
#     if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
#         return True
#     else:
#         return False
#
# if __name__=="__main__":
#     ustring=u'中国 人名ａ高频Ａ'
#     # 判断是否有其他字符；
#     for item in ustring:
#         if (is_other(item)):
#             break


if __name__ == "__main__":
    ustring = u'中国 人名ａ高频Ａ'
    # 判断是否有其他字符；
    for item in ustring:
        if (is_other(item)):
            break

    print ishan(u'abd你')