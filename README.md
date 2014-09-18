## Update Bootloader by ble for board nrf51

### How to

Setup the board

```sh
git submodule update --init --recursive
make flash
```

Disable the bootloader mode

```sh
make disable-bootloader
```

### Documentation

 * [wiki](https://github.com/astraliot/ble-bootloader/wiki)
