import requests
from datetime import datetime
from retrying import retry
from database import DBSession, Config
from urllib.parse import quote
import logging
import json

try:
    session = DBSession()
    config = session.query(Config).get(1)
    TG_ON = config.tg_push_on
    TG_CHAT_ID = config.tg_chatid
    TG_BOT_TOKEN = config.tg_bot_token
    BARK_ON = config.bark_push_on
    BARK_TOKENS = config.bark_tokens.split(',')
    SERVER_CYANN_ON = config.server_cyann_on
    SERVER_CYANN_TOKEN = config.server_cyann_token
    PROXY = config.proxy_on
    PROXY_URL = config.proxy_url
    session.close()
except Exception as e:
    exit(1)


# Telegram
@retry(stop_max_attempt_number=3, wait_fixed=1000)
def telegram(info_dict, mid):
    md_text = '*{} {} （{}）*\n\n“{}” [@豆瓣]({})\n\n评分: {}\n' \
        .format(info_dict['basic']['title'], info_dict['basic']['original_title'], info_dict['basic']['year'], info_dict['basic']['intro'],
                info_dict['basic']['douban_url'], info_dict['basic']['douban_rating'])

    url = 'https://api.telegram.org/bot{}/sendMessage'.format(TG_BOT_TOKEN)
    data = {'chat_id': TG_CHAT_ID, 'text': md_text,
            'parse_mode': 'markdown', 'disable_notification': True}
    headers = {'Content-Type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0'}
    try:
        if PROXY:
            r = requests.post(url, headers=headers, data=json.dumps(
                data), proxies={'http': PROXY_URL, 'https': PROXY_URL})
        else:
            r = requests.post(url, headers=headers, data=json.dumps(data))
    except Exception as e:
        return False
    return True


# Bark(IOS)
def bark(info_dict, mid):
    success_count = 0
    fail_count = 0
    if int(info_dict['basic']['year']) >= datetime.now().year - 1:
        pre_title = '上新'
    else:
        pre_title = '上旧'
    title = '{}：[{}]{}（{}）'.format(
        pre_title, info_dict['basic']['_type'], info_dict['basic']['title'], info_dict['basic']['year'])
    for token in BARK_TOKENS:
        if token=='':
            continue
        url = 'https://api.day.app/{}/{} {} ({}) {}分/点击查看'.format(
            token, title, info_dict['basic']['original_title'], info_dict['basic']['year'], info_dict['basic']['douban_rating'])
        try:
            r = requests.get(url)
            if r.json()['code'] == 200:
                success_count += 1
            else:
                fail_count += 1
        except Exception:
            fail_count += 1 
    return success_count, fail_count


# Server酱
def server_cyann(info_dict, mid):
    if int(info_dict['basic']['year']) >= datetime.now().year - 1:
        pre_title = '上新'
    else:
        pre_title = '上旧'
    title = '{}：[{}]{}（{}）'.format(
        pre_title, info_dict['basic']['_type'], info_dict['basic']['title'], info_dict['basic']['year'])
    content = ''
    url = 'https://sctapi.ftqq.com/{}.send?title={}&desp={}'.format(
        SERVER_CYANN_TOKEN, title, quote(content, safe=''))
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0'}
    r = requests.get(url, headers=headers)
    if r.json()['code'] == 0:
        return True
    return False


# 推送
def run(info, mid):
    res_result = ''
    # Telegram
    if TG_ON:
        tg_result = telegram(info, mid)
        res_result += 'Telegram发送成功, ' if tg_result else 'Telegram发送失败, '
    # Bark
    if BARK_ON:
        bark_success_count, bark_fail_count = bark(info, mid)
        res_result += 'Bark{}成功{}失败, '.format(
            bark_success_count, bark_fail_count)
    #
    if SERVER_CYANN_ON:
        result = server_cyann(info, mid)
        res_result += 'Server酱发送成功，' if result else 'Server酱发送失败'

    logging.info(res_result)
