#!/usr/bin/env python
#-*- coding: utf-8 -*-
import urllib
import urllib2
import hashlib
import os
import random
import mimetypes  
import mimetools
import time
import config

config = config.config()

def get_content_type(filepath):  
    return mimetypes.guess_type(filepath)[0] or 'application/octet-stream'  
  
def encode_multipart_formdata(fields, files=[]):  
    """ 
    fields is a sequence of (name, value) elements for regular form fields. 
    files is a sequence of (name, filepath) elements for data to be uploaded as files 
    Return (content_type, body) ready for httplib.HTTP instance 
    """  
    #BOUNDARY = mimetools.choose_boundary()
    BOUNDARY = '----WebKitFormBoundaryiNvFjH83d9Ga5l8k'
    CRLF = '\r\n'  
    L = []  
    for key in fields:  
        L.append('--' + BOUNDARY)  
        L.append('Content-Disposition: form-data; name="%s"' % key)  
        L.append('')  
        L.append(fields[key])  
    for key in files:  
        L.append('--' + BOUNDARY)  
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, os.path.basename(files[key])))  
        L.append('Content-Type: %s' % get_content_type(files[key]))  
        L.append('')  
        L.append(open(files[key], 'rb').read())  
    L.append('--' + BOUNDARY + '--')  
    L.append('')  
    body = CRLF.join(L)  
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY  
    return content_type, body

def getCurrentTime():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def logger(level,action,data):
    global config
    dirt = {'INFO':6,'WARNING':3,'ERROR':1,'OFF':0}
    configLevel = dirt[config.logLevel]
    currentLevel = dirt[level]
    if configLevel >= currentLevel:
        currentTime = getCurrentTime()
        color = "\033[3%im"%currentLevel
        print color+currentTime+" ["+level+"]\033[0m"
        print "\033[32m|== "+action+" ==\033[0m "+data
    
def login(opener,headers):
    global config
    request = urllib2.Request('http://nian.so',None,headers)
    response = opener.open(request)
    out = response.read()
    response.close(); 
    
    em = config.em
    #em = 'scpc11@vip.qq.com'
    pw = 'n*A'+config.pw
    #pw = 'n*A'+'784278688a'
    pw = hashlib.md5(pw).hexdigest()
    data = {'em':em,'pw':pw}
    data = urllib.urlencode(data) 

    logger('INFO','LOGIN',data)
  
    request = urllib2.Request('http://nian.so/login_check.php',data,headers)
    response = opener.open(request)
    out = response.read()
    response.close();
    return opener

def getDreamId(opener,headers):
    request = urllib2.Request('http://nian.so/list.php',None,headers)
    response = opener.open(request)
    out = response.read()
    info = response.info()
    response.close(); 
    #print info
    st_index = out.find('thing.php?id=')
    st_index += 13
    ed_index = out.find('\')">\n\n<!--乱入-->')
    if st_index <= 13:
        dream_id = 'no_dream_id_catched'
    else:
        dream_id = out[st_index:ed_index]
    logger('INFO','GetDreamId',dream_id)
    return dream_id

def addStep(opener,headers):
    global config
    dream_id = getDreamId(opener,headers)
    if dream_id == 'no_dream_id_catched':
        return ;
    if config.withPic != 'NULL':
        files = {'up3':'rpi.jpg'}
        fields = {'sub3':'提交'}

        content_type,body = encode_multipart_formdata(fields,files)
        '''
        headers = {
            'Host':'nian.so',
            'Connection':'keep-alive',
            'Cache-Control':'max-age=0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Origin':'http://nian.so',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
            'Content-Type':content_type,
            'Referer':'http://nian.so',
            'Accept-Encoding':'gzip,deflate',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
            'Cookie':'Cookie:PHPSESSID=d6e0qt3rgre8botmh3opma71c6; uid=117401; shell=8d93da2b74a2f480644ac692dc1f1901; ref=http://nian.so/; __utmt=1; __utma=6360749.913152218.1412997538.1412998124.1413011405.3; __utmb=6360749.11.10.1413011405; __utmc=6360749; __utmz=6360749.1412997538.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            'RA-Ver':'2.6.2',
            'RA-Sid':'7AE08DEA-20140705-115110-914e8a-cce45a'
            }
        '''
        upload_headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
            'Content-Type':content_type,
            'Referer':'http://nian.so'
            }
        

        #print headers
        #print body
        request = urllib2.Request('http://nian.so/yun_step.php',body,upload_headers)
        response = opener.open(request)
        out = response.read()
        info = response.info()
        response.close()

        st_index = out.find('ccess("')
        st_index += 7
        if st_index <= 7:
            logger('ERROR','UploadImg','Upload operation failed.')
            return ;
        ed_index = out.find('")</sc')
        upload_src = out[st_index:ed_index]
        
        logger('INFO','UploadImgGetSrc',upload_src)

        img_array = upload_src.split('+')
        img = img_array[0]
        img0 = img_array[1] #img width
        img1 = img_array[2] #img height
    else:
        img = ''
        img0 = '' 
        img1 = ''

    content = '更新内容'
    key = '不同步'

    dream = dream_id
    t = random.random()
    content = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    data = {'content':content,
            'key':key,
            'img':img,
            'img0':img0,
            'img1':img1,
            'dream':dream,
            't':t}
    data = urllib.urlencode(data) 
    
    logger('INFO','AddStep',data)

    request = urllib2.Request('http://nian.so/addstep_query.php',data,headers)
    response = opener.open(request)
    out = response.read()
    response.close();
     
    logger('INFO','AddStep','result:'+out)

def checkComment(opener,headers):
    print ""

def sendComment(opener,headers):
    content = '测试评论'
    dream_id = '146790'
    t = random.random()
    data = {'content':content,'id':dream_id,'t':t}
    data = urllib.urlencode(data)

    logger('INFO','SendComment',data)

    request = urllib2.Request('http://nian.so/comment_query.php',data,headers)
    response = opener.open(request)
    out = response.read()
    response.close()

    #data = {'id':
    #request = urllib2.Request('http://nian.so/push/push_web.php',data,headers)
    #print ""

if __name__ == '__main__':
    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    headers = {'Referer':'http://nian.so','User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'}
    opener = login(opener,headers)
	
    commandList = ['check_comment','send_comment']

    for command in commandList:
        if command == 'check_comment':
            checkComment(opener,headers)
        elif command == 'send_comment':
            sendComment(opener,headers)
        elif command == 'add_step':
            addStep(opener,headers)
    
    print ""   
    raw_input("press enter key to continue >>>")
