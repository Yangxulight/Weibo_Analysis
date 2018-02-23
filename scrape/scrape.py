import requests
import base64
import re
import urllib
import urllib.parse
import rsa
import json
import binascii
from bs4 import BeautifulSoup
import 

class WeiboScape:
    def __init__(self, username, password):
        self.url_login = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)"
        self.username = username
        self.password = password
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0"
        }

    # pre login for sina page. return a json data with nonce,pubkey, servertime, rsakv
    # all the json data will be used in login function
    def pre_login(self):
        session = requests.Session()
        session.get(self)
        json_pattern = re.compile('\((.*)\)')
        try:
            request = urllib.request.Request(self.get_pre_login_url())
            response = urllib.request.urlopen(request)
            raw_data = response.read().decode('utf-8')
            json_data = json_pattern.search(raw_data).group(1)
            data = json.loads(json_data)
            return data
        except urllib.error as e:
            print("%d" % e.code)
            return None

    def get_pre_login_url(self):
        url_pre_login = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="+ self.get_encrypted_username +"&rsakt=mod&client=ssologin.js(v1.4.5)&_=1364875106625"
        return url_pre_login


    def get_encrypted_username(self):
        encode_username = urllib.request.quote(self.username)
        encrypted_username = base64.b64encode(encode_username.encode(encoding='utf-8'))
        return encrypted_username

    def get_encrypted_password(self, nonce, servertime, pubkey):
        password_full = str(nonce) + '\t' + str(servertime) + '\n' + self.password
        rsa_enpoment = 0x10001
        key = rsa.PublicKey(int(pubkey,16),rsa_enpoment)
        encrypted_password = rsa.encrypt(password_full, key)
        return encrypted_password

    def create_post_data(self,data):
        post_form = {
            "entry": "weibo",
            "gatewary": "1",
            "from": "",
            "savestate": "7",
            "qrcode_flag": "false",
            "useticket": "1",
            "pagerefer": "https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F",
            "vsnf": "1",
            "su": self.get_encrypted_username(),
            "service": "miniblog",
            "servertime": data['servertime'],
            "nonce": data['nonce'],
            "pwencode": 'rsa2',
            "rsakv": data['rsakv'],
            "sp": self.get_encrypted_password(),
            "sr": "1440*900",
            "encoding": "UTF-8",
            "prelt": "316",
            "url": "https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "returntype": "META"
        }
        data = urllib.parse.urlencode(post_form).encode('utf-8')

    def enableCookie(self):
        # setup a container
        cookie_saver = http.cookiejar.CookieJar()
        # bind the container to a http cookie processor
        cookie_support = urllib.request.HTTPCookieProcessor(cookie_saver)
        # create a opener to open a url
        opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)

    def login(self):
        self.enableCookie()
        data = self.pre_login()
        post_data = self.create_post_data(data)
        try:
            request = urllib.request.Request(url=url, data=post_data, headers=self.headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode('GBK')
            print(html)
        except urllib.error as e:
            print(e.code)

if __name__ == '__main__':
    username = "yangxulight@outlook.com"
    password = "light3768"
    scrape = WeiboScape(username,password)
    scrape.login()
    




        




