#!/bin/sh
url=`python3 pickurl.py`
wget -O dl.iso $url
7z x -o/var/www/iso dl.iso
cp /var/www/iso/images/pxeboot/initrd.img /var/tftpboot/pxelinux/initrd.img
cp /var/www/iso/images/pxeboot/vmlinuz /var/tftpboot/pxelinux/vmlinuz
chown -R /var/www nginx:nginx 
rm dl.iso
