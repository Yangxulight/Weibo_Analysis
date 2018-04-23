from weibo_data import WeiboData


if __name__ == "__main__":
    file_list = ['user_list4.txt', 'user_list5.txt']
    crawler = WeiboData()
    for filename in file_list:
        crawler.fetch_user_data(filename)