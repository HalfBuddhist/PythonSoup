#!/usr/bin/env python
# coding=utf-8

import sys, time

if __name__ == '__main__':
    begin_clock = time.clock()
    sys.stdin = open('../in.txt', 'r')
    # sys.stdout = open('out.txt', 'w')
    # presolve
    # input
    a = input()
    # b = input()
    print len(a)
    # print len(a)
    # print len(b)
    # print len(b[0])
    # for i in b:
    #     print i,
    for b in a:
        print b

    # resolve
    # output
    # print time.clock() - begin_clock