# Modified version of sdk file
SDK_SRCS += dfu_dual_bank.c
SDK_SRCS += bootloader.c
SDK_SRCS += ble_dfu.c
SDK_SRCS += hci_mem_pool.c
SDK_SRCS += app_timer.c
SDK_SRCS += app_scheduler.c
SDK_SRCS += app_gpiote.c
SDK_SRCS += crc16.c
SDK_SRCS += softdevice_handler.c
SDK_SRCS += app_button.c
SDK_SRCS += nrf_delay.c
SDK_SRCS += ble_conn_params.c
SDK_SRCS += ble_advdata.c
SDK_SRCS += ble_srv_common.c
SDK_SRCS += bootloader_util_gcc_cuss.c
SDK_SRCS += dfu_transport_ble_PCA10001.c
SDK_SRCS += pstorage_cortex.c

APPLICATION_SRCS += src/gcc_aeabi.c
APPLICATION_SRCS += src/main.c
APPLICATION_SRCS += $(SDK_SRCS)

PROJECT_NAME = uBootUpdater
PROJECT_BOOTLOADER = true

DEVICE = NRF51
BOARD = BOARD_PCA10001

USE_SOFTDEVICE = s110

EXTERNAL_PATH = $(MAKEFILE_DIR)/external
SDK_PATH = $(MAKEFILE_DIR)
MAKEFILE_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
TEMPLATE_PATH = $(MAKEFILE_DIR)/nrf51-pure-gcc-setup/template/
SOFTDEVICE = $(EXTERNAL_PATH)/s110_nrf51822_7.0.0_softdevice.hex

SOURCE_PATHS  += src sdk_modified
LIBRARY_PATHS += include

#CFLAGS  = -O2
CFLAGS  = -DDEBUG -g3 -O0 -I . -Werror

GDB_PORT_NUMBER = 2331

include $(TEMPLATE_PATH)/Makefile
