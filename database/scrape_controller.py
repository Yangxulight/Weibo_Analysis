from weibo_data import WeiboData


if __name__ == "__main__":
    file_list = ['user_list7.txt']
    crawler = WeiboData()
    for filename in file_list:
        crawler.fetch_user_data(filename)