import os
import time
import base64
import hashlib
import time


NGINX_CONF_FILE = '/etc/nginx/nginx.conf'


def get_secure_passwd():
    with open('./.secure_password') as f:
        secure_passwd = f.read()
    return secure_passwd


def gen_movie_links(url_prefix, secure_passwd, video_files_str):
    def gen_md5(text, isBackByte=False):
        md5 = hashlib.md5()
        if isinstance(text, bytes):
            md5.update(text)
        else:
            md5.update(text.encode('utf-8'))
        if isBackByte:
            return md5.digest()
        return md5.hexdigest()

    def base64_encode(text, isBytes=False):
        if isBytes:
            return base64.b64encode(text)
        return base64.b64encode(bytes(text, encoding="utf-8"))

    links = []
    for video_file in video_files_str.split(',/'):
        path = url_prefix + video_file.lstrip('/')
        endtime = int(time.time()) + 3600 * 4
        res = gen_md5(str(endtime) + str(path) +
                      ' ' + str(secure_passwd), True)
        md5 = str(base64_encode(res, True))
        md5 = md5.replace('b\'', '').replace('\'', '').replace(
            '+', '-').replace('/', '_').replace('=', '')
        links.append('{}?md5={}&expires={}'.format(path, md5, endtime))
    return links
