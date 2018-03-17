from weibo_data import WeiboData


if __name__ == "__main__":
    crawler = WeiboData()
    crawler.fetch_user_data()