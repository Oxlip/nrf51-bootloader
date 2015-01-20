import os
import sys
import subprocess

from nrftool.command.jlink import ExecJLinkScriptCommand

class JLinkInfo(ExecJLinkScriptCommand):

   SCRIPT = 'info.jlink'

   def execute(self):
      return super(JLinkInfo, self).execute(self.SCRIPT)

class NRF51(object):

   def __init__(self):
      self.tty_name = self._found_board_tty()

   def _found_board_tty(self):
      return '/dev/ttyACM0'

   def is_available(self):
      if os.path.exists(self.tty_name):
         return False

      res = True
      command = JLinkInfo()
      sys.exit(command.execute())
      print 'fff'
      return res

   def reboot(self):
      pass

   def reset(self):
      pass
 
