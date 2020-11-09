# 本地检索路径(如/mnt/Media/)
ROOT_DIR = ''

# 资源链接前缀(如http://192.168.x.x:xxx/media/、ftp://192.168...)
PRE_URI = ''

# 播放链接前缀
PLAY_URI = ''

# 资源链接后缀(避免路径不对无法访问的情况)
AFTER_URI = '/'

# 命名正则(包含（豆瓣中文）标题和年份，默认为电影名、中文括号年份，如：灰猎犬号（2020）)
MOVIE_DIR_RE = '(.*?)（(\d{4})）'

# 页面标题
PAGE_TITLE = 'Movie DB'

# 浏览链接(页面侧栏浏览按钮对应链接)
BROWSER_LINK = ''

# 本程序URL
URL = 'http://127.0.0.1:5001'