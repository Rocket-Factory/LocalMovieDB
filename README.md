# LocalMovieDB
基于豆瓣信息的（简易）本地电影数据库（Web），用于NAS电影检索。(<del>由于原来流传豆瓣API key权限没收,可能无法使用</del>)。
新的分支已解决该问题，并提供了API（详见`douban.py`）


## 功能
- 获取本地电影豆瓣信息（可定时运行）
- 推送新电影消息至Telegram和Bark
- Web页面展示电影列表和播放页面（调用PC、移动端视频软件）
- 标题搜索、排序、Tag筛选

![PC0](https://raw.githubusercontent.com/Rocket-Factory/LocalMovieDB/master/preview/PC0.png)
![MB0](https://raw.githubusercontent.com/Rocket-Factory/LocalMovieDB/master/preview/PC1.png)
![MB1](https://raw.githubusercontent.com/Rocket-Factory/LocalMovieDB/master/preview/MB0.png)
![MB1](https://raw.githubusercontent.com/Rocket-Factory/LocalMovieDB/master/preview/MB1.png)


## 使用
1. 创建Python3虚拟环境，安装依赖。
2. 创建配置文件`config.py`，注意命名正则。
3. 运行`app.py`，手动执行`job.py`获取电影信息。
4. 创建cron任务，定时执行`job.py`更新电影信息。

## 注意
1. 电影路径格式要求：默认（可自行设置正则）为`豆瓣电影名（年份）`，路径内需存在视频文件。
2. 评论功能需要手动输入消息链接，需要科学上网查看。
3. 豆瓣API会去获取新的电影和剧集，如不存在可能会导致数据库收录和推送失败，建议先打开`https://alagorn.8610000.xyz/api/v1/movie/豆瓣Subject ID`查看是否存在（不存在会自动加入服务器队列，半个小时后再查看应该就有了）。
4. 服务器资源十分有限，仅方便个人整理和分享，请勿滥用。

## 更新
### 2020-12-28
- `legolas`分支重写了Web页面
- 适配Potplayer和VLC（移动端）
- 合并推送功能（TansmissionNotify不再更新）
- 新增绑定Telegram消息评论功能（需公开群组或频道）
- 修复BUG

### 2020-11-10
- 修复API问题
- 新增视频app快捷播放页面
- 新增简介
