from logging import CRITICAL, ERROR,  WARN, INFO, DEBUG
from logging import critical, error, info, warning, warn, debug
from logging import Formatter, getLogger, StreamHandler
import sys
import os
import datetime

global ANSI
ANSI = {
    'gray' : lambda text: '\033[1;30m' + unicode(text) + '\033[1;m',
    'red' : lambda text: '\033[1;31m' + unicode(text) + '\033[1;m',
    'green' : lambda text: '\033[1;32m' + unicode(text) + '\033[1;m',
    'yellow' : lambda text: '\033[1;33m' + unicode(text) + '\033[1;m',
    'blue' : lambda text: '\033[1;34m' + unicode(text) + '\033[1;m',
    'magenta' : lambda text: '\033[1;35m' + unicode(text) + '\033[1;m',
    'cyan' : lambda text: '\033[1;36m' + unicode(text) + '\033[1;m',
    'white' : lambda text: '\033[1;37m' + unicode(text) + '\033[1;m',
    'bgred' : lambda text: '\033[1;41m' + unicode(text) + '\033[1;m',
    'bggreen' : lambda text: '\033[1;42m' + unicode(text) + '\033[1;m',
    'bgbrown' : lambda text: '\033[1;43m' + unicode(text) + '\033[1;m',
    'bgblue' : lambda text: '\033[1;44m' + unicode(text) + '\033[1;m',
    'bgmagenta' : lambda text: '\033[1;45m' + unicode(text) + '\033[1;m',
    'bgcyan' : lambda text: '\033[1;46m' + unicode(text) + '\033[1;m',
    'bggray' : lambda text: '\033[1;47m' + unicode(text) + '\033[1;m',
    'bgyellow' : lambda text: '\033[1;43m' + unicode(text) + '\033[1;m',
    'bggrey' : lambda text: '\033[1;100m' + unicode(text) + '\033[1;m'
}


class ANSIFormatter(Formatter):
    """
    Convert a `logging.LogReport' object into colored text, using ANSI escape sequences.
    """
    ## colors:
    
    @property
    def now(self):
        return datetime.datetime.now().strftime(' %H:%M:%S ')

    def format(self, record):
        _d = {'INFO': 'cyan', 'WARNING': 'yellow', 'ERROR':'red',
              'CRITICAL': 'bgred', 'DEBUG': 'bggrey'}
        if record.levelname in _d.keys():
            return ANSI[_d[record.levelname]](record.levelname) + ANSI['green'](self.now) + ANSI['white'](record.msg)
        else:
            return ANSI['white'](record.levelname) + ANSI['green'](self.now) + ANSI['white'](record.msg)


class TextFormatter(Formatter):
    """
    Convert a `logging.LogReport' object into text.
    """

    def format(self, record):
        if not record.levelname or record.levelname is 'INFO':
            return record.msg
        else:
            return record.levelname + ': ' + record.msg


class DummyFormatter(object):
    """
    A dummy class.
    Return an instance of the appropriate formatter (ANSIFormatter if sys.stdout.isatty() is True, else TextFormatter)
    """

    def __new__(cls, *args, **kwargs):
        if os.isatty(sys.stdout.fileno()): # thanks to http://stackoverflow.com/questions/2086961/how-can-i-determine-if-a-python-script-is-executed-from-crontab/2087031#2087031
            return ANSIFormatter(*args, **kwargs)
        else:
            return TextFormatter( *args, **kwargs)





def init(level=None, logger=getLogger(), handler=StreamHandler()):
    fmt = DummyFormatter()
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    if level:
        logger.setLevel(level)


init(level=DEBUG)

if __name__ == '__main__':
    init(level=DEBUG)
    debug('debug')
    info('info')
    warning('warning')
    error('error')
    critical('critical')


__all__ = [
    "debug", 
    "info", 
    "warn", 
    "warning",
    "error", 
    "critical", 
    "DEBUG", 
    "INFO", 
    "WARN", 
    "ERROR", 
    "CRITICAL"
] 
