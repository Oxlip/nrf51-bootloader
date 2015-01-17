import os.path

class NRF51(object):

   def __init__(self):
      self.tty_name = self._found_board_tty()      

   def _found_board_tty(self):
      return '/dev/ttyACM0'

   def is_connect(self):
      return os.path.exists(self.tty_name)

   def reboot(self):
      pass

   def reset(self):
      pass
 
