import logbook

from web.locatsettings import Config


class SingletonDecorator:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance


@SingletonDecorator
class Log(object):

    def __init__(self, name='Guodou', filename=Config.LOGS_NAME):
        """

        :param name: 项目名称
        :param filename: log文件名称
        """
        self.handler = logbook.FileHandler(filename, encoding='utf-8')
        logbook.set_datetime_format('local')  # 将日志时间设置为本地时间
        self.logger = logbook.Logger(name)
        self.handler.push_application()

    def info(self, *arg, **kwargs):
        """返回Log info信息"""
        self.logger.info(*arg, **kwargs)

    def error(self, *arg, **kwargs):
        """返回报错信息"""
        self.logger.error(*arg, **kwargs)

    def warning(self, *arg, **kwargs):
        """返回警告信息"""
        self.logger.warning(*arg, **kwargs)

    def debug(self, *arg, **kwargs):
        """返回调试信息"""
        self.logger.debug(*arg, **kwargs)

