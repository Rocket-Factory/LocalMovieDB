# LocalMovieDB
基于豆瓣信息的（简易）本地电影数据库（Web），用于NAS电影检索。


## 功能
- 抓取本地电影豆瓣信息（可设置定时运行）
- 推送新电影消息至Telegram、Bark、Server酱
- Web页面展示电影列表和播放页面（调用PC、移动端视频APP）
- 标题搜索、排序、Tag筛选

![PC0](https://raw.githubusercontent.com/Rocket-Factory/LocalMovieDB/legolas/preview/PC0.jpg)
![MB0](https://raw.githubusercontent.com/Rocket-Factory/LocalMovieDB/legolas/preview/PC1.jpg)
![MB1](https://raw.githubusercontent.com/Rocket-Factory/LocalMovieDB/legolas/preview/mb0.jpg)
![MB1](https://raw.githubusercontent.com/Rocket-Factory/LocalMovieDB/legolas/preview/mb1.jpg)


## 使用
1. 创建Python3虚拟环境，安装依赖。
2. 创建配置文件`config.py`，注意命名正则。
3. 运行`app.py`，手动执行`job.py`获取电影信息。
4. 创建cron任务，定时执行`job.py`更新电影信息。

## 注意
1. 电影路径格式要求：默认（可自行设置正则）为`豆瓣电影名（年份）`，路径内需存在视频文件。
2. 评论功能需要手动输入消息链接，需要科学上网查看。
3. 豆瓣API会去获取新的电影和剧集，如不存在可能会导致数据库收录和推送失败，详见`https://douban.8610000.xyz/`。

## 更新
### 2021-05-15
1. 修复UI的各种BUG
2. 添加PWA提示

### 2021-04-09
1. UI优化（IOS PWA）
2. 移除fileserver
3. 修复重复推送Bug

### 2021-02-21
1. UI更新（主要是详情页）
2. 修复滚动加载的Bug
3. 新增自带fileserver（仅X86）
4. 新增Server酱推送
5. 数据库结构变化，需要删除db文件重新获取

### 2021-01-17
1. 切换API到Github Pages，避免服务器流量问题

### 2021-01-03
1. 修复bug，优化细节
2. 支持IOS PWA（Safari 添加到主屏幕）
3. 详情页返回不再重载首页
4. 新增IINA播放

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
