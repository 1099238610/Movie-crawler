
<center>
    
![Movie-crawler](https://github.com/1099238610/Movie-crawler/blob/main/img/icon.jpg)

<img src="https://img.shields.io/badge/python-3.10.0-green?logo=python" alt="Author" /> <img src="https://img.shields.io/badge/scrapy-2.6.2-blue" alt="Author" /> <img src="https://img.shields.io/github/languages/top/1099238610/Movie-crawler?color=yellow" alt="languages-top" />

</center>

# 🎬电影爬虫工具
用于爬取电影网站上的各种数据

## 豆瓣爬虫

### 介绍
目前可以爬取豆瓣 TOP250 的电影名称和评分

### 使用方法
1. 使用 git clone 命令克隆项目
2. 使用命令运行豆瓣爬虫
    ```
   scrapy crawl douban_movies -o movie.json
   ```
   
## IMDB爬虫

### 介绍
世界上最大的电影数据库, 目前支持爬取电影基本英文信息

| 字段 | 解释 |
| ---------|----------|
| title | 电影名称 | 
| rating | 评分, 范围 0 - 10 |
| year | 上映年份 |
| duration |  电影时长, 格式为 h mm, 例如 1h 25m |
| MPA_rating | MPA 电影分级, 分为 G、PG、PG-13、R 和NC-17 |


### 使用方式
1. 命令行使用 git clone 命令克隆项目
    ```
    git clone https://github.com/1099238610/Movie-crawler
    ```
2. 使用命令运行豆瓣爬虫
    ```
   scrapy crawl IMDB -o IMDB_movie.json
   ```
3. 在统计目录下会生成 IMDB_movie.json 的电影信息文件

### 考虑添加的功能
1. 电影数据翻译为中文
2. 支持不同类型的格式存储, 如 excel, csv
