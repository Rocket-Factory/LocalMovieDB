import os
import re
import logging

realpath = os.path.split(os.path.realpath(__file__))[0]


def search_video_files(path, files):
    for file_ in os.listdir(path):
        if os.path.isfile(os.path.join(path, file_)):
            if file_.split('.')[-1] in ['mp4', 'mkv', 'ts', 'flv'] and not file_.startswith('.'):
                files.append(os.path.join(path, file_))
            continue
        search_video_files(os.path.join(path, file_), files)


def search_movie(movie_dir_re, root_dir, path, movies):
    for file_ in os.listdir(path):
        if not os.path.isdir(os.path.join(path, file_)):
            continue
        re_result = re.match(movie_dir_re, file_)
        if re_result:
            video_files = []
            search_video_files(os.path.join(path, file_), video_files)
            video_files.sort()
            video_files = [video_file[len(root_dir):]
                           for video_file in video_files]
            video_files_str = ','.join(video_files)
            logging.debug('找到视频文件: {}'.format(video_files_str))
            if video_files_str != '' and (re_result.group(1), re_result.group(2), os.path.join(path, file_), video_files_str) not in movies:
                movies.append((re_result.group(1), re_result.group(
                    2), os.path.join(path, file_), video_files_str))
        search_movie(movie_dir_re, root_dir, os.path.join(path, file_), movies)
