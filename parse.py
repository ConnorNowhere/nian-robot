#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import string

def parseNotice(noticeText):
    #rule = re.compile(ur'\d+&&comment\'\)">(\w+|[\u4e00-\u9fa5]+)')
    rule = re.compile(ur'\d+&&comment\'\)">.+')
    array = rule.findall(unicode(noticeText,'utf-8')) 
    for val in array:
        print val
    print "----"
    rule = re.compile(ur'uid=\d+\'\)">.+</span></a>.+')
    array = rule.findall(unicode(noticeText,'utf-8'))
    for val in array:
        print val

if __name__ == "__main__":
    f = open('./test','r')
    ncText = f.read()
    f.close()
    parseNotice(ncText)
