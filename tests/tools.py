import os
import json
import logging.config

TEST_FAILED  = 1
TEST_SUCCESS = 0

class TestLogger(logging.Logger):

   PASSED  = logging.INFO + 1
   FAILED  = logging.INFO + 2
   TIMEOUT = logging.INFO + 3

   def __init__(self, name):
      logging.addLevelName(self.PASSED, 'PASSED')
      logging.addLevelName(self.FAILED, 'FAILED')
      logging.addLevelName(self.TIMEOUT, 'TIMEOUT')
      super(TestLogger, self).__init__(name)

   def passed(self, msg, *args, **kw):
      self.log(self.PASSED, msg, *args, **kw)

   def failed(self, msg, *args, **kw):
      self.log(self.FAILED, msg, *args, **kw)

   def timeout(self, msg, *args, **kw):
      self.log(self.TIMEOUT, msg, *args, **kw)

class TestFormatter(logging.Formatter):
   color = {
    'INFO'   : 4,
    'TIMEOUT': 3,
    'PASSED' : 2,
    'FAILED' : 1,
    'ERROR'  : 1,
   }

   def __init__(self, _format):
      super(TestFormatter, self).__init__(_format)

   def _colorize(self, string):
      return '\033[3{}{}{}\033[0m'.format(self.color[string], ";1m", string)

   def format(self, record):
      if record.levelname in self.color:
         record.levelname = self._colorize(record.levelname)
      return super(TestFormatter, self).format(record)

logpath='configs/logging.json'
logging.setLoggerClass(TestLogger)
logger = logging.getLogger('Test')
if os.path.exists(logpath):
   with open(logpath, 'rt') as f:
      config = json.load(f)
   logging.config.dictConfig(config)
else:
   logging.basicConfig(level=logging.INFO)


g_driver = None
def getDriver(driver = None):
   if driver is not None:
      g_driver = driver
   return g_driver

g_board = None
def getBoard(board = None):
   if board is not None:
      g_board = board
   return g_board
