### Web配置
URL = 'http://xxx.xx' # 本程序URL

USERS = [(1, 'user1', 'passwd1'),(2,'user2','passwd2')] # 访问账户

SECRET_KEY = 'yoursecret' # 秘钥(仅加密token用)

ROOT_DIR = '/mnt/Media/' # 本地检索路径(如/mnt/Media/)

PLAY_URI = 'http://user:passwd@192.x.x.xx:port/xxxx' # # 播放链接URI(HTTP,FTP等服务路径，用于构造如下播放链接 http://user:password@192.168.2.2/share/电影/未归类/西方/灰猎犬号（2020）/Greyhound.2020/Greyhound.mkv)

MOVIE_DIR_RE = '(.*?)（(\d{4})）' # 命名正则(包含（豆瓣中文）标题和年份，默认为电影名、中文括号年份，如：灰猎犬号（2020）)

COMMENTS_ON  = False  # 加载Telegram评论(页面上可设置评论消息地址)

### 推送

# 启用Telegram推送
TG_ON = False
TG_CHAT_ID = 123456 # chat id（群组、频道、或用户）
TG_BOT_TOKEN = '' # telegram bot token

# 代理(对Telegram推送生效)
PROXY = False
PROXY_URL = 'http://127.0.0.1:7890'

# 启用Bark(IOS)推送
BARK_ON = False
BARK_TOKENS = ['',] # Bark Token列表
