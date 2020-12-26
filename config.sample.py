# 访问账户
USERS = [(1, 'user1', 'passwd1'),(2,'user2','passwd2')]

# 秘钥(加密token用)
SECRET_KEY = 'yoursecret'

# 本地检索路径(如/mnt/Media/)
ROOT_DIR = '/mnt/Media/'

# 播放链接URI(HTTP,FTP等服务路径，用于构造如下播放链接 http://user:password@192.168.2.2/share/电影/未归类/西方/灰猎犬号（2020）/Greyhound.2020/Greyhound.mkv)
PLAY_URI = 'http://user:passwd@192.x.x.xx:port/xxxx'

# 命名正则(包含豆瓣中文标题和年份，默认为电影名、中文括号年份，如：灰猎犬号（2020）)
MOVIE_DIR_RE = '(.*?)（(\d{4})）'

# Telegram评论
COMMENTS_ON  = False

