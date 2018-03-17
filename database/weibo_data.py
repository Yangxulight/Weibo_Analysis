import re
import requests
from bs4 import BeautifulSoup
from database.cookie import Cookie
import time
from mongodb import MongoDB
import datetime
from utils.scrape_logger import scrape_logger as logger
import json

class WeiboData:
    login_url = "https://weibo.cn"
    weibo_base_url = "https://weibo.cn/u/{}?filter=1&page={}"
    info_base_url = "https://weibo.cn/{}/info"
    username = "yangxulight@outlook.com"
    password = "light3768"
    info_pattern = re.compile('<div class="c">昵称:(.*)<br/>性别:(.*)<br/>地区:(.*)<br/>生日:(.*?)<br/>')
    weibo_pattern = re.compile('<div><span class="ctt">(.*?)</span>.*?赞\[([0-9]*)\].*?转发\[([0-9]*)\].*?评论\[([0-9]*)\].*?<span class="ct">(.*?)</span>')
    weibo_page_pattern = re.compile('<input name="mp" type="hidden" value="([0-9]*)" />')
    userlist_pattern = re.compile('action-data="uid=([0-9]*)')
    basic_pattern = re.compile('<span class="tc">微博\[([0-9]*)\].*?关注\[([0-9]*)\].*?粉丝\[([0-9]*)\]') # number of weibo, following, fans
    weibo_scheme = {
        'uid': '',
        'info': {
            'username': '',
            'gender': '',
            'region': '',
            'birth': ''
        },
        'weibos':[{
            'content': '',
            'like': '',
            'repost': '',
            'comment': '',
            'datetime': ''
        }],
        'basic': {
            'weibo_num': '',
            'following': '',
            'fans': ''
        }
    }

    user_scheme = {
        'uid': '',
        'last_fetched': ''
    }

    def fetch_user_list(self):
        with open("user_list.txt",'w') as fo, open('user_w.txt','w') as fw:
            html = fo.read()
            fo.close()
            users = self.userlist_pattern.findall(html)
            users = list(set(users))
            for user in users:
                fw.writelines(str(user))
        return users


    def build_request(self, cookies):
        logger.debug("building request with cookies".format(cookies))
        request = requests.Session()
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'}
        request.headers.update(headers)
        for cookie in cookies:
            request.cookies.set(cookie['name',cookie['value']])
        return request

    def fetch_user_info(self, uid, request, timeout):
        info_url = self.info_base_url.format(uid,1)
        time.sleep(timeout)
        logger.debug("fetching user info from {}".format(uid))
        response = request.get(info_url)
        matchObj = self.info_pattern.search(response.content.decode('utf-8'))
        info = {}
        info['username'] = matchObj.group(1)
        info['gender'] = matchObj.group(2)
        info['region'] = matchObj.group(3)
        info['birth'] = matchObj.group(4)
        return info

    def fetch_user_weibo(self, uid, request, timeout):
        logger.debug("fetching weibo content from {}".format(uid))
        weibos = []
        weibo_url = self.weibo_base_url.format(uid, 1)
        time.sleep(timeout)
        logger.debug("fetching weibo from {} at page {}".format(uid, 1))
        response = request.get(weibo_url)
        max_page_obj = self.weibo_page_pattern.search(response.content.decode('uft-8'))
        if max_page_obj is None:
            max_page = 1
        else:
            max_page = int(max_page_obj.group(1))
        weibo_list = re.findall(self.weibo_page_pattern, response.decode('utf-8'))
        for w in weibo_list:
            weibo = {}
            weibo['content'] = w[0]
            weibo['like'] = w[1]
            weibo['repost'] = w[2]
            weibo['comment'] = w[3]
            weibo['datetime'] = w[4]
            weibos.append(weibo)
        for i in range(2, max_page+1):
            weibo_url = self.weibo_base_url.format(uid, i)
            time.sleep(timeout)
            logger.debug("fetching weibo from {} at page {}".format(uid, i))
            response = request.get(weibo_url)
            weibo_list = re.findall(self.weibo_page_pattern, response.content.decode('utf-8'))
            for w in weibo_list:
                weibo = {}
                weibo['content'] = w[0]
                weibo['like'] = w[1]
                weibo['repost'] = w[2]
                weibo['comment'] = w[3]
                weibo['datetime'] = w[4]
                weibos.append(weibo)
        return weibos

    def fetch_basic_data(self, uid, request, timeout=2):
        basic = {}
        url = self.weibo_base_url.format(uid, 1)
        time.sleep(timeout)
        logger.debug("fetching basic data from {}".format(uid))
        response = request.get(url)
        basic_boj = self.basic_pattern.search(response.content.decode('utf-8'))
        basic['weibo_num'] = basic_boj.group[1]
        basic['following'] = basic_boj.group[2]
        basic['fans'] = basic_boj.group[3]
        return basic 

    def fetch_user_data(self, timeout=2):
        db = MongoDB(host="localhost", port=27017)
        logger.debug("fetch userlist from db")
        fetched_users = { item['uid'] for item in db.query(collection='user',db_name='weibo_database',condition="")}
        uid_list = [item for item in self.fetch_user_list and item not in fetched_users]
        cookies = Cookie.load_cookies()
        request = self.build_request(cookies)
        with open("cache/weibodata.txt", 'a+') as d, open("cache/userdata.txt", 'a+') as u:
            for uid in uid_list:
                data = {}
                data['uid'] = uid
                data['weibos'] = self.fetch_user_weibo(uid, request, timeout)
                data['info'] = self.fetch_user_info(uid, request,timeout)
                data['basic'] = self.fetch_basic_data(uid, request, timeout)
                user = {}
                user['uid'] = uid
                user['last_fetched'] = datetime.datetime.now()
                db.save_document(collection="weibo",db_name="weibo_database", data)
                db.save_document(collection='user', db_name='weibo_database', user)
                data_json = json.dumps(data)
                user_json = json.dumps(user)
                f.write(data_json+'\n')
                u.write(user_json+'\n')
                
        
            









        


        
        

