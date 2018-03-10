# Database setup
This doc will tell you how to install mongodb and setup you machine to make sure our project can deploy correctly.
- ## Mongodb Installation
    #### 1. Max OS
    Download your mongodb on this page: https://www.mongodb.org/
Then, unzip your file to the path you want to install, such as:```/Users/Ryan/MongoDB ```
Make a dir to store your data, such as:```~/myProject/Weibo_Analysis/database```
Open the bin dir in your installation dir, such as:```cd /Users/Ryan/MongoDB/bin ```, then ```./mongod --dbpath <path-to-your-store> ```, you will see something like ```waiting for connections on port 27017 ```, which means your mongodb is installed correctly.

    You may need more info from [here](https://github.com/StevenSLXie/Tutorials-for-Web-Developers/blob/master/MongoDB%20%E6%9E%81%E7%AE%80%E5%AE%9E%E8%B7%B5%E5%85%A5%E9%97%A8.md).
- ## Python3 support
You need to install pymongo by ```pip install pymongo ```

- ## Collection design


