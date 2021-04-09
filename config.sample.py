## Web配置
URL = 'http://192.x.x.xx:5011' # 本程序URL(如使用反代可自行修改)

USERS = [(1, 'user', 'passwd'),] # Web访问账户

SECRET_KEY = 'yoursecret' # 秘钥(仅加密token用,可随意设置)

ROOT_DIR = '/mnt/Media/' # 本地检索路径(如/mnt/Media/)

# 播放视频的URI
PLAY_URI = 'http://{}:{}@192.x.x.xx:xxxx/share'.format(USERS[0][1], USERS[0][2]) # 播放链接URI(可根据情况自行修改)

# 电影文件夹正则表达式, 用于识别
MOVIE_DIR_RE = '(.*?)（(\d{4})）' # 命名正则(包含（豆瓣中文）标题和年份，默认为电影名、中文括号年份，如：灰猎犬号（2020）)

## 代理(用于Telegram推送、TMDB API)
PROXY = False
PROXY_URL = 'http://127.0.0.1:7890'


## 推送
# 启用Telegram推送
TG_ON = False
TG_CHAT_ID = 123456 # chat id（群组、频道、或用户）
TG_BOT_TOKEN = '' # telegram bot token

# 启用Bark(IOS)推送
BARK_ON = False
BARK_TOKENS = ['',] # Bark Token列表


# 启用Server酱
SERVER_CYANN_ON = False
SERVER_CYANN_TOKEN = ''