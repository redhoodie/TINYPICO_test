#! /bin/bash
rshell -a --buffer-size=32 -p /dev/cu.SLAB_USBtoUART -b 115200 --file sync.rshell
