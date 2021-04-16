'''
    Mooc 总项目的配置文件
'''

import os
import re
import sys

# DEBUG_URL = "https://www.icourse163.org/course/HIT-154005?tid=1450314458"
DEBUG_URL = ""
DEBUG_QUALITY = "1"
# DEBUG_QUALITY = ""

COOKIE_FILE = "cookie.txt"

if hasattr(sys, 'frozen'):
    PATH = os.path.dirname(sys.executable)
else:
    PATH = os.path.dirname(os.path.abspath(__file__))  # 程序当前路径
winre = re.compile(r'[?*|<>:"/\\\s]')  # windoes 文件非法字符匹配
WIN_LENGTH = 64
TIMEOUT = 60  # 请求超时时间
PLAYLIST = '播放列表.dpl'
PALYBACK = 'DPL_PYJUN'
BATNAME = '修复播放列表.bat'
BATSTRING = '''\
@echo off
copy {0} {1}
echo 成功修复“{1}”
echo 请用Potplayer播放器打开“{1}”观看视频（未安装Potplayer自行百度下载安装）
pause
'''.format(PALYBACK, PLAYLIST)
LENGTH = 80

# 变量，可修改的参数
download_speed = "1248K"
if getattr(sys, 'frozen', False):  # 是否打包
    aria2_path = os.path.join(sys._MEIPASS, "aria2c.exe")
else:
    aria2_path = os.path.join(PATH, "aria2c.exe")
aira2_cmd = '%s -x 16 -s 64 -j 64 -k 2M --disk-cache 128M {header} "{url:}" -d "{dirname:}" -o "{filename:}"' % (
    aria2_path,)
m3u8_cmd = 'ffmpeg -i "{url:}" -c copy -bsf:a aac_adtstoasc {filename:}'

# 课程链接的正则匹配
courses_re = {
    "icourse163_mooc": re.compile(r'\s*https?://www.icourse163.org/((learn)|(course))/(.*?)(#/.*)?$'),
    "icourse_cuoc": re.compile(r'\s*https?://www.icourses.cn/web/sword/portal/videoDetail\?courseId=([\w-]*)'),
    "icourse_mooc": re.compile(r'\s*((https?://www.icourses.cn/sCourse/course_(\d+).html)|'
                               r'(https?://www.icourses.cn/web/sword/portal/shareDetails\?cId=(\d+)))')
}

__all__ = [
    "DEBUG_QUALITY", "DEBUG_URL",
    "COOKIE_FILE",
    "PATH", "winre", "TIMEOUT", "PLAYLIST", "PALYBACK",
    "BATNAME", "BATSTRING", "LENGTH", "WIN_LENGTH",

    "download_speed", "aria2_path", "aira2_cmd", "m3u8_cmd", "courses_re"
]
