SDK_SRCS += dfu_dual_bank.c
SDK_SRCS += bootloader.c
SDK_SRCS += ble_dfu.c
SDK_SRCS += hci_mem_pool.c
SDK_SRCS += app_timer.c
SDK_SRCS += app_scheduler.c
SDK_SRCS += app_gpiote.c
SDK_SRCS += crc16.c
SDK_SRCS += softdevice_handler.c
SDK_SRCS += pstorage.c
SDK_SRCS += app_button.c
SDK_SRCS += nrf_delay.c
SDK_SRCS += ble_conn_params.c
SDK_SRCS += ble_advdata.c
SDK_SRCS += ble_srv_common.c

# Modified version of sdk file
SDK_SRCS += bootloader_util_arm_gcc.c
SDK_SRCS += dfu_transport_ble_PCA10001.c
SDK_SRCS += bootloader_settings_arm_gcc.c


APPLICATION_SRCS = src/main.c $(SDK_SRCS)
PROJECT_NAME = uBootUpdater
PROJECT_BOOTLOADER = true

DEVICE = NRF51
BOARD = BOARD_PCA10001

USE_SOFTDEVICE = s110

SDK_PATH = /opt/nrf51sdk/nrf51822/
MAKEFILE_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
TEMPLATE_PATH = $(MAKEFILE_DIR)/nrf51-pure-gcc-setup/template/
SOFTDEVICE = s110_nrf51822_7.0.0_softdevice.hex

SOURCE_PATHS  += src sdk_modified
LIBRARY_PATHS += include
LIBRARY_PATHS += $(SDK_PATH)/Include/bootloader_dfu
LIBRARY_PATHS += $(SDK_PATH)/Include/bootloader_dfu/hci_transport

CFLAGS = -DDEBUG -g3 -O0 -I . -Werror

GDB_PORT_NUMBER = 2331

include $(TEMPLATE_PATH)/Makefile
