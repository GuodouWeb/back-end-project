import logbook

from web.middleware.decorator import SingletonDecorator


@SingletonDecorator
class Log(object):

    handler = None

    def __init__(self, name='interfaceAutomation', filename="InterfaceAutomation.config['LOG_NAME']"):
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
        return self.logger.info(*arg, **kwargs)

    def error(self, *arg, **kwargs):
        """返回报错信息"""
        return self.logger.error(*arg, **kwargs)

    def warning(self, *arg, **kwargs):
        """返回警告信息"""
        return self.logger.warning(*arg, **kwargs)

    def debug(self, *arg, **kwargs):
        """返回调试信息"""
        return self.logger.debug(*arg, **kwargs)