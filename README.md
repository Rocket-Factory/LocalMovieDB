# LocalMovieDB
基于豆瓣信息的（简易）本地电影数据库（Web），用于NAS电影检索。(<del>由于原来流传豆瓣API key权限没收,可能无法使用</del>)。
新的分支（alagorn）已解决该问题，并提供了API（详见`douban.py`）


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


## 更新
### 2020-11-10
- 修复API问题
- 新增视频app快捷播放页面
- 新增简介
