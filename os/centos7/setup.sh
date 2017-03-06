#!/bin/sh
url=`python3 pickurl.py`
wget -O dl.iso $url
xorriso --osirrox on -indev dl.iso -extract / /var/www/iso
cp /var/www/iso/images/pxeboot/initrd.img /var/tftpboot/pxelinux/initrd.img
cp /var/www/iso/images/pxeboot/vmlinuz /var/tftpboot/pxelinux/vmlinuz
chown -R nginx:nginx /var/www
rm dl.iso
