'''
    Mooc 的请求模块：包含 get, post, head 常用的三大请求
'''

import os
from functools import wraps
from socket import timeout, setdefaulttimeout
from time import sleep
from urllib import request, parse
from urllib.error import ContentTooShortError, URLError, HTTPError
import requests

from Mooc.Mooc_Config import *

__all__ = [
    'RequestFailed', 'request_get', 'request_post'
]

headers = [("User-Agent",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")]

if os.path.isfile(COOKIE_FILE):
    with open(COOKIE_FILE) as file:
        cookie_str = file.read()
    headers.append(("Cookie", cookie_str))

aria2_header_params = " ".join('--header="{}"'.format(x) for x in [": ".join(x) for x in headers])

opener = request.build_opener()
opener.addheaders = headers
request.install_opener(opener)
setdefaulttimeout(TIMEOUT)


class RequestFailed(Exception):
    pass


def retry_when_failed(count=3):
    def decorate(func):
        @wraps(func)
        def wrap_func(*args, **kwargs):
            cnt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except (ContentTooShortError, URLError, HTTPError, ConnectionResetError) as err:
                    print(err)
                    cnt += 1
                    if cnt >= count:
                        break
                    sleep(0.32)
                except (timeout):
                    break
            raise RequestFailed("request failed")

        return wrap_func

    return decorate


@retry_when_failed()
def request_get(url, decoding='utf8'):
    '''get请求'''
    req = request.Request(url=url)
    response = request.urlopen(req, timeout=TIMEOUT)
    text = response.read().decode(decoding)
    response.close()
    return text


@retry_when_failed()
def request_post(url, data, decoding='utf8'):
    '''post请求'''
    headers = {
        "Cookie": 'CLIENT_IP=223.73.111.130; close_topBar=1; learningplan1033945722=false; EDUWEBDEVICE=1a537df538364d24aa67e234f00d2821; WM_TID=F6XXK73EiNFBFRAUABYuOvnB6nX7oNPH; __yadk_uid=qhQatWaunFkPJOvXbBTSUAfbLTVD4U99; NTESSTUDYSI=7098f483c5ca4c03aedc0b763d97f07f; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1614521104,1614568902; NETEASE_WDA_UID=1033945722#|#1511769393763; bpmns=1; hasVolume=true; videoVolume=0.8; CLIENT_IP=223.73.111.130; MOOC_PRIVACY_INFO_APPROVED=true; __utma=63145271.544993581.1614671680.1614671680.1614671680.1; __utmc=63145271; __utmz=63145271.1614671680.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); STUDY_SESS="MoVrdaFLzD7KR5qnYGpOQeIw+KF6RAvMKCHGmg5MvfBRB6uMZjEzYH9uIj2+s6xYASLGRx9l6cUSG89VLPgvcpTLs2ltvUEGyVylorkE2y9QjzEAI+e9yv67keKR23Sj277yyooWnSQHw73h/eOUJ3MUU1YcuE8zLdnt1RQWJENwTReNbq3Ao4r8auiHuvMb+P6MxCmnJEvne6pPMc9TTJJnThNrM7aj0X5LVpSBvjY+jLUkiE0tBwSGBJj2yGvmCj7amAaDbJJnC264ceZEklEbRRmZ7J82Zgp4KqVxxrBKlOh/Gwx6G1S/X4FQ7qd/vJK/atoXOXkc3/E+/0gD2JhOkBORJAZW8xlFI7iAqScYDQgUHxPU94Uw2p0fb10Y"; STUDY_INFO=UID_A8F428A4978FE3077D81BC8D2CF7C31E|4|1033945722|1614847747580; videoRate=2; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1614952229; WM_NI=pBaJF1QQ7XSeMkXLDoAFp%2BOVwo%2FzIFjpJKfcWx46v0FBjAyHNiuuvaD6R8QeTetJ4aYLBuIvjeApiRZ9wigsEAk1Qi6NW5mc5gC29f8WwJ3qCSZrCzR530zVJTho%2B1fvNW0%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed2e474bc88aaccee72ace78eb7d15b868f8f85f56d868ab69ab763a5b68f98aa2af0fea7c3b92ab49eafabc53b938ff9b9d26f8fb598adc765839ac0ccce5eb5b1e19bcc4eaab086ace56995a8fcd7f53c869ea6a2fc448eb7bb96f56b88ea9ed9d46f98bbbcabb76b9b948e96cc7eaabb8f91ec5a9ae7b98ae679879fa5d2d463f69299d6f069f7b98dd3bc6efc89b9abb27b818d9693c27292ebfdd1f95e8a8ca890aa3ba6aa82b8b337e2a3'
    }
    # requests.post(url=url, data=data, headers=headers)
    data = parse.urlencode(data).encode('utf8')
    req = request.Request(url=url, data=data, method='POST', headers=headers)
    response = request.urlopen(req, timeout=TIMEOUT)
    text = response.read().decode(decoding)
    response.close()
    return text

