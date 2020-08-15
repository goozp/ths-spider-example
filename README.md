# ths-spider-example
完整的 Scrapy 爬虫示例，爬取股票和新闻数据。

本项目爬取同花顺股票信息和新闻，为作者硕士在读时提供研究数据，仅作研究用途，爬取手段及其温柔，且都为公开信息，研究结束即已停止使用。现只作为 Scrapy 爬虫 demo，仅供作为教程使用。

参考：[Python3网络爬虫开发实战](https://python3webspider.cuiqingcai.com/)

技术栈：
- Python (Scrapy)
- MongoDB

实现的爬虫：
- ths-stock 股票信息
- ths-stock-daily 股票当日交易信息
- ths-stock-news 股票下的新闻
- ths-news 7x24小时滚动新闻

## 部署

### 环境要求
本项目使用 Docker 部署。
- Docker
- Docke-compose
- Git

构建后的容器：
- 爬虫 Spider：qs-spider
- 数据库 MongoDB：qs-mongo

### 下载
```
git clone https://github.com/goozp/ths-spider-example.git
```

### 修改配置
- Docker 环境配置： `.env`

- Mongo 配置：`mongodb/docker-entrypoint-initdb.d/mongo-init.js`
    ```
    db.createUser(
        {
            user: "user",
            pwd: "userpwd",
            roles: [
                {
                    role: "readWrite",
                    db: "stock"
                }
            ]
        }
    );
    ```
    修改 `user` 和 `pwd`，初始化创建的用户名和密码。
- 爬虫配置：`spiders/quan_sys_spiders/settings.py`
    ```
    MONGO_URI = 'mongodb://user:userpwd@qs-mongo/stock'
    MONGO_DATABASE_STOCK = 'stock'
    ```

### 构建并启动
```
cd ths-spider-example
docker-compose up -d
```

注：MongoDB 在 Windows 下不能使用 `./data/mongo:/data/db` 绑定数据卷；只能以另一种绑定形式存在：`mongodata:/data/db`
使用这种模式，在 Linux 中的数据存储在: `/var/lib/docker/volumes/quan-sys-env_mongodata`

启动后将会开始定时爬取数据。每天晚上九点执行：
```
scrapy crawl ths-stock
scrapy crawl ths-stock-daily
scrapy crawl ths-stock-news
```

每两分钟执行：
```
scrapy crawl ths-news
```

### 关闭和开启
```
docker-compose stop
docker-compose start
```

### 删除容器再构建
```
docker-compose down
docker-compose up -d
```
测试阶段增加 -v 参数，删除绑定的数据卷，上线后不要这样做：
```
docker-compose down -v
docker-compose up -d
```

### 其它操作

#### 进入 Spider 容器，手动执行 Spider
```
docker exec -it qs-spider /bin/bash
```

Start Spider:
```
scrapy crawl ths-stock
```