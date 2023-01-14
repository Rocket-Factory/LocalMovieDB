import logging
import time
from datetime import datetime

from utils import sql_util, scrape_util, movie_search_util


class UpdateTask:
    def __init__(self):
        self.is_running = False
        now = datetime.now()
        self.last_run_all_time = datetime.timestamp(now)
        self.messages = []

    def save_and_show_log(self, level, text):
        logging.log(level, text)
        prefix = time.strftime('%Y-%m-%d %H:%m:%S {} '.format(level))
        self.messages.append(prefix + text)

    def get_current_msg(self):
        return self.messages[-1][22:]

    def update_movie_data(self):
        self.is_running = True
        self.messages = []
        
        run_all_flag = False
        now = datetime.now()

        # 每5天更新全部数据
        if datetime.timestamp(now) - self.last_run_all_time >= 432000:
            run_all_flag = True

        if not sql_util.get_setting_value('inited'):
            self.save_and_show_log(logging.INFO, '---数据库未初始化,结束任务---')
            self.is_running = False
            return
        
        self.save_and_show_log(logging.INFO,'---影视数据更新任务开始---')
        self.messages.append('---影视数据更新任务开始---')
        if not scrape_util.q_file_exists() or scrape_util.q_file_expired():
            self.save_and_show_log(logging.INFO, '缓存不存在或超期,获取API电影数据...')
            scrape_util.download_q_file()
        q_movies = scrape_util.read_q_file()
        self.save_and_show_log(
            logging.INFO, '已获取，共{}条电影数据'.format(len(q_movies)))
        movies = []
        root_dir = sql_util.get_setting_value('root_dir')
        movie_dir_re = sql_util.get_setting_value('movie_dir_re')
        movie_search_util.search_movie(
            movie_dir_re, root_dir, root_dir, movies)
        movie_path_list = []
    
        for index, movie in enumerate(movies):
            title, year, path_, video_files_str = movie
            relative_path = path_[len(root_dir):]
            movie_path_list.append(relative_path)
            logging.debug(
                '[{}/{}]获取电影: {}'.format(index, len(movies), path_))
            
            if sql_util.movie_exists(year, relative_path, video_files_str) and not run_all_flag:
                logging.debug('已收录，跳过')
                continue
            
            self.save_and_show_log(
                logging.INFO, '开始削刮电影: {} ({})'.format(title, year))
            mid = scrape_util.get_movie_id(q_movies, title, year)
            if not mid:
                self.save_and_show_log(
                    logging.WARNING, '获取豆瓣ID出错,数据库可能尚未收录,跳过...')
                continue
            movie_info_json = scrape_util.get_movie_info(mid)
            if not movie_info_json:
                self.save_and_show_log(logging.ERROR, '获取豆瓣影视信息出错,跳过...')
                continue
            movie_info_json['uri'] = relative_path
            movie_info_json['video_files'] = video_files_str
            sql_util.update_or_insert_movie(movie_info_json)
        self.save_and_show_log(logging.INFO, '清理失效数据...')
        sql_util.remove_deleted_movies(movie_path_list)
        self.save_and_show_log(logging.INFO, '---影视数据更新任务结束---')
        
        if run_all_flag:
            now = datetime.now()
            self.last_run_all_time = datetime.timestamp(now)
        self.is_running = False

    def run(self, interval):
        while not self.is_running:
            try:
                self.update_movie_data()
            except Exception as e:
                logging.exception('---本次任务运行出错---')
            
            time.sleep(interval)
