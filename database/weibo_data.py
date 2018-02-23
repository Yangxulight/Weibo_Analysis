import re

class WeiboData:
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
        pass

    @classmethod
    def save_cookie(cls):
        

        
        

