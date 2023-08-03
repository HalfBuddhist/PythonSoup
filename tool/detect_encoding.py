#!/usr/bin/env python
# coding=utf-8

if __name__ == '__main__':
    import chardet
    f = open('template/vimrc', 'rb')
    text = f.read()
    info = chardet.detect(text)
    print(info)
