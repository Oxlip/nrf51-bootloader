#!/bin/env python
#
# 1) reset the board with the ttyACM0
# 2) tests all the ble char available <---------------------|
# 3) upload the new app to run                              |
# 4) switch on the test_app_vX                              | test_app_v{1,2,3}
# 5) control all the test_app_vX ble action                 |
# 6) switch back to the bootloader to load test_app_vX+1 -->|
# 7) reset the board with the ttyACM0
# 8) test the test_app3

import os
import sys
import time
import json
import logging
from tools import logger, TEST_FAILED, TEST_SUCCESS, getBoard, getDriver
from nrf51 import NRF51

from ble_tools.udriver import ubledriver
from ble_tools.udriver import datahelper

def get_name(driver):
   time.sleep(2)
   umsg = { 'dest_id' : '#fake_serial', 'action' : 'infos' }
   res = driver.send_umsg(umsg)

   name_handle = None
   main_serv = res['services'][0]
   for char in main_serv['char']:
      if char['uuid'] == '0x2803':
         if char['value']['uuid'] == 'DEVINCE_NAME':
            name_handle = char['value']['handle']

   if name_handle is None:
      logger.failed('Unable to found the device name')
      return None
  
   umsg['action'] = 'read'
   umsg['handle'] = name_handle
   name = driver.send_umsg(umsg)
   return name    



class TestApp:

   app_name_fmt = 'test_app_{stage}'

   def __init__(self, stage):
      self.stage    = stage
      self.app_name = self.app_name_fmt.format(stage = stage)

   def load(self, driver):
      umsg = {
         'dest_id' : '#fake_serial',
         'action'  : 'dfu',
         'file'    : sys.argv[1]
      }

      if not os.path.exists(umsg['file']):
         logger.error('Unable to found the file \'%s\'', umsg['file'])
         return

      file_stat = os.stat(umsg['file'])
      umsg['file_size'] = file_stat.st_size

      if not driver.send_umsg(umsg):
         logger.failed('Unable to load the new app %s', umsg['file'])
         return 

      logger.passed('%s: app is loaded', self.app_name)

   def test(self, driver):
      name = get_name(driver)
      if not name == 'uPlug':
         logger.failed('The device is not the dfu [%s]', name)
      else:
         logger.passed('dfu: Charracterristic test passed')


class DFUTest:

   def dfu_switch(self):
     logger.passed('dfu: switch to dfu mode done')

   def dfu_test(self):
      name = get_name(self.driver)
      if not name == 'DfuTarg':
         logger.failed('The device is not the dfu [%s]', name)
      else:
         logger.passed('dfu: Charracterristic test passed')

   def precheck(self):
      board = NRF51()

      if not board.is_available():
         logger.error('Unable to contact the board')
         sys.exit(TEST_FAILED)

      driver = ubledriver.uBleDriver()
      driver.init()

      if not driver.is_init():
         logging.error('Unable to initialize ble driver')
         sys.exit(TEST_FAILED)

      driver.run()

      self.board  = board
      self.driver = driver

      logger.passed('precheck done')

   def start(self):
      logger.info('DFU functional test start')
      res = TEST_SUCCESS

      self.precheck()

      self.board.reset()

      for idx in range(3):
         try:
            if idx is not 0:
               self.dfu_switch()
            self.dfu_test()
            app = TestApp(idx)
            app.load(self.driver)
            app.test(self.driver)
         except Exception, e:
            logger.exception(e)
            res = TEST_FAILED

      self.board.reboot()
      app.test(self.driver)

      return res

if __name__ == '__main__':
   test = DFUTest()
   try:
      res = test.start()
   except Exception, e:
      logger.exception(e)
      res = TEST_FAILED
   except:
      logger.info('Tests have exit')
      res = TEST_FAILED
   finally:
      sys.exit(res)
