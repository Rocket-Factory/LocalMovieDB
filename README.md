# LocalMovieDB
基于豆瓣信息的（简易）本地电影数据库（Web），用于NAS电影检索。(**由于原来流传豆瓣API key权限没收,可能无法使用**)


## 功能
- 获取本地电影豆瓣信息（可定时运行）
- Web页面展示缩略图、信息、路径
- 标题搜索、排序、多Tag筛选

![PC](https://raw.githubusercontent.com/Rocket-Factory/LocalMovieDB/master/preview/0.png)
![MB0](https://raw.githubusercontent.com/Rocket-Factory/LocalMovieDB/master/preview/1.png)
![MB1](https://raw.githubusercontent.com/Rocket-Factory/LocalMovieDB/master/preview/2.png)


## 使用
1. 创建Python3虚拟环境，安装依赖。
2. 创建配置文件`config.py`，注意命名正则。
3. 运行`app.py`，手动执行`job.py`获取电影信息。
4. 创建cron任务，定时执行`job.py`更新电影信息。
