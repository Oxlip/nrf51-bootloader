import os
import sys
import tempfile
import subprocess

from tools import logger

JLINK_ERRORS = {
   "Can not connect to J-Link via USB.": "Can not find the device.",
   "ERROR: Could not open file.": "Can not find the specified firmware.",
   "Syntax:": "The script contain an syntax error"
}

class JLinkError(Exception):
   def __init__(self, text, linenumber):
      self.text = text
      self.linenumber = linenumber

   def __str__(self):
      return self.text

class ExecJLinkScriptCommand(object):

   def __init__(self, verbose = False, jlinkexe = 'JLinkExe', **kwargs):
      self.verbose = verbose
      self.jlinkexe = jlinkexe

   def execute(self, script, **kwargs):
      if len(kwargs) > 0:
         script = self.create_tmp_script(script, **kwargs)

      try:
         if not os.path.exists(script):
            raise JLinkError('script \'{script}\' not found'.format(script = script), -1)
         output = subprocess.check_output([self.jlinkexe, script],
                                          universal_newlines = True,
                                          stderr = subprocess.STDOUT)
      except subprocess.CalledProcessError as exception:
         output = exception.output

      return self.process_output(output, self.verbose)

   def create_tmp_script(self, script, **kwargs):
      content = open(script, "r").read().decode("utf-8")
      stream = content.format(**kwargs).encode("utf-8")

      with tempfile.NamedTemporaryFile(delete=False) as f:
         name = f.name
         f.write(stream)

      return name

   def process_output(self, output, verbose):
      lines = output.split("\n")

      for i, line in enumerate(lines):
         for err in JLINK_ERRORS:
            if line.startswith(err):
               raise JLinkError(line, i)

      if verbose:
         print(output)

      return lines

   def colorize(self, s):
      return "\033[01;31m" + s + "\033[00m"

class JLinkFlash(ExecJLinkScriptCommand):

   FLASH_SD   = 0
   FLASH_UICR = 1
   FLASH_APP  = 2

   scripts = {
      FLASH_SD   : 'scripts/flash-sd.jlink',
      FLASH_UICR : 'scripts/flash-uicr.jlink',
      FLASH_APP  : 'scripts/flash-app.jlink'
   }

   firmwares = {
      FLASH_SD   : '../_build/s110_nrf51822_7.0.0_softdevice.bin',
      FLASH_UICR : '../_build/uBootUpdater_s110-uirc.bin',
      FLASH_APP  : '../_build/uBootUpdater_s110.bin'
   }

   addresses = {
      FLASH_SD   : 0,
      FLASH_UICR : 0x10001014,
      FLASH_APP  : 0
   }

   def __init__(self, ftype, firmware = None, address = None, **kwargs):
      super(JLinkFlash, self).__init__(**kwargs)
      self.ftype = ftype
      self.firmware = self.format_firmware(firmware)
      self.address = self.format_address(address)   

   def execute(self):
      return super(JLinkFlash, self).execute(self.scripts[self.ftype],
                                             firmware = self.firmware,
                                             address = self.address)

   def format_firmware(self, firmware):
      if not firmware:
         firmware = self.firmwares[self.ftype]
      return os.path.abspath(firmware)

   def format_address(self, address):
      if not address:
         address = self.addresses[self.ftype]
      try:
         return hex(int(address))
      except ValueError:
         return address


class JLinkInfo(ExecJLinkScriptCommand):
   SCRIPT = 'scripts/info.jlink'

   def execute(self):
      lines = super(JLinkInfo, self).execute(self.SCRIPT)

      res = {}
      for line in lines:
         if line.startswith('Firmware:'):
            res['firmware'] = line.rstrip()
         if line.startswith('Hardware:'):
            res['hardware'] = line.rstrip()

      return res


class JLinkReboot(ExecJLinkScriptCommand):
   SCRIPT = 'scripts/reboot.jlink'

   def execute(self):
      return super(JLinkReboot, self).execute(self.SCRIPT)

class NRF51(object):

   def __init__(self):
      self.tty_name = self._found_board_tty()

   def _found_board_tty(self):
      return '/dev/ttyACM0'

   def is_available(self):
      try:
         command = JLinkInfo()
         resp = command.execute()
         logger.info(resp['firmware'])
         logger.info(resp['hardware'])
      except JLinkError, e:
         logger.error(e.text)
         return False

      if not os.path.exists(self.tty_name):
         logger.error('tty not found: %s', self.tty_name)
         return False

      return True

   def reboot(self):
      cmd = JLinkReboot()
      cmd.execute()

   def reset(self):
      cmd = JLinkFlash(JLinkFlash.FLASH_SD)
      cmd.execute()
      cmd = JLinkFlash(JLinkFlash.FLASH_UICR)
      cmd.execute()
 
