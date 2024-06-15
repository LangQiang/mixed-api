"""
封装log方法

"""

import os
import time
import logging.handlers

# 日志打印等级
LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

# 创建一个日志
logger = logging.getLogger()
level = 'default'


# 创建日志文件方法
def create_file(filename):
    path = filename[0:filename.rfind('/')]
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.isfile(filename):
        fd = open(filename, mode='w', encoding='utf-8')
        fd.close()
    else:
        pass


# 给logger添加handler 添加内容到日志句柄中
def set_handler(levels):
    if levels == 'error':
        logger.addHandler(MyLog.err_handler)
    logger.addHandler(MyLog.handler)


# 在记录日志之后移除句柄
def remove_handler(levels):
    if levels == 'error':
        logger.removeHandler(MyLog.err_handler)
    logger.removeHandler(MyLog.handler)


def get_current_time():
    return time.strftime(MyLog.date, time.localtime(time.time()))


class MyLog:
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = path + '/log.log'
    err_file = path + '/err.log'
    logger.setLevel(LEVELS.get(level, logging.NOTSET))
    create_file(log_file)
    create_file(err_file)
    date = '%Y-%m-%d %H:%M:%S'

    # 创建一个handler，用于写入日志文件
    handler = logging.handlers.RotatingFileHandler(log_file, mode='a', maxBytes=1024 * 1024 * 256, backupCount=2,
                                                   encoding='utf-8')
    err_handler = logging.handlers.RotatingFileHandler(err_file, mode='a', maxBytes=1024 * 1024 * 256, backupCount=2,
                                                       encoding='utf-8')

    @staticmethod
    def debug(log_meg):
        set_handler('debug')
        # 文件中输出模式
        logger.debug(get_current_time() + " [DEBUG] \t" + log_meg + "\n")
        remove_handler('debug')

    @staticmethod
    def info(log_meg):
        set_handler('info')
        logger.info(get_current_time() + " [INFO]  \t" + log_meg + "\n")
        remove_handler('info')

    @staticmethod
    def warning(log_meg):
        set_handler('warning')
        logger.warning(get_current_time() + " [WARNING] \t" + log_meg + "\n")
        remove_handler('warning')

    @staticmethod
    def error(log_meg):
        set_handler('error')
        logger.error(get_current_time() + " [ERROR] \t" + log_meg + "\n")
        remove_handler('error')

    @staticmethod
    def critical(log_meg):
        set_handler('critical')
        logger.error(get_current_time() + " [CRITICAL] \t" + log_meg + "\n")
        remove_handler('critical')

    @staticmethod
    def log_flask_request(request, g):
        g.start = time.time()
        log_str = 'Request: %s %s %s \n' % (request.remote_addr, request.url, request.method)
        for header in request.headers:
            log_str = '%s Header: %s: %s\n' % (log_str, header, request.headers.get(header))
        log_str = '%s Param: %s: \n' % (log_str, dict(request.args))
        MyLog.info(log_str)

    @staticmethod
    def log_flask_response(response, g):
        response_time = time.time() - g.start
        log_str = 'Response  status: %s Content-Length: %s time: %.3f \n' % (response.status_code, len(response.data), response_time * 1000)
        log_str = log_str + str(response.data, 'utf-8')
        MyLog.info(log_str)

    # 设置控制台输出格式
    formatter = logging.Formatter('%(message)s')
    # 再创建一个handler，用于输出到控制台
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    console.setLevel(logging.NOTSET)


if __name__ == "__main__":
    MyLog.debug(
        "This is debug messageThis is debug messageThis is debug messageThis is debug messageThis is debug messageThis is debug messageThis is debug messageThis is debug message")
    MyLog.info("This is info message")
    MyLog.warning("This is warning message")
    MyLog.error("This is error")
    MyLog.critical("This is critical message")
