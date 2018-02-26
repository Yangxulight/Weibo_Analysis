import re
from database.cookie import Cookie
import requests

class WeiboData:
    login_url = "https://weibo.cn"
    base_url = "https://weibo.cn/u/{}"
    username = "yangxulight@outlook.com"
    password = "light3768"
    @classmethod
    def fetch_user_list(cls):
        pattern = re.compile('action-data"')
        with open("user_list.txt",'w') as fo, open('user_w.txt','w') as fw:
            html = fo.read()
            fo.close()
            users = pattern.findall(html)
            users = list(set(users))
            for user in users:
                fw.writelines(str(user))
        return users

    @classmethod
    def fetch_user_weibo(cls, uid):
        uid_list = WeiboData.fetch_user_list()
        cookies = Cookie.load_cookies()
        request = self.build_request(cookies)
        for uid in uid_list:
            page_url = base_url.format(uid)
            response = request.get(page_url)
            self.save_data(response.content)


    def build_request(self, cookies):
        request = requests.Session()
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'}
        request.headers.update(headers)
        for cookie in cookies:
            request.cookies.set(cookie['name',cookie['value']])
        return request

    def save_data(self, data):
        pass


        
        

