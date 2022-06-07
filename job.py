import logging
import time

from utils import sql_util, scrape_util, movie_search_util


class UpdateTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, interval):
        while self._running:
            if not sql_util.get_setting_value('inited'):
                logging.info('---数据库未初始化，等待中...---')
                time.sleep(interval)
                continue
            logging.info('---影视数据更新任务开始---')
            if not scrape_util.q_file_exists() or scrape_util.q_file_expired():
                logging.info('缓存不存在或超期，获取API电影数据...')
                scrape_util.download_q_file()
            q_movies = scrape_util.read_q_file()
            logging.info('已获取，共{}条电影数据'.format(len(q_movies)))

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
                if sql_util.movie_exists(year, relative_path, video_files_str):
                    logging.debug('已收录，跳过')
                    continue
                logging.info('开始削刮电影: {} ({})'.format(title, year))
                mid = scrape_util.get_movie_id(q_movies, title, year)
                if not mid:
                    logging.warning('获取豆瓣ID出错，数据库可能尚未收录')
                    continue
                movie_info_json = scrape_util.get_movie_info(mid)
                if not movie_info_json:
                    logging.error('获取豆瓣影视信息出错')
                    continue
                movie_info_json['uri'] = relative_path
                movie_info_json['video_files'] = video_files_str
                sql_util.update_or_insert_movie(movie_info_json)

            
            logging.info('清理失效数据...')
            sql_util.remove_deleted_movies(movie_path_list)

            logging.info('---影视数据更新任务结束---')

            time.sleep(interval)
