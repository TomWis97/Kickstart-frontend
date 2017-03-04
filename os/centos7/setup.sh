#!/bin/sh
url='http://mirror.netrouting.net/centos/7/isos/x86_64/CentOS-7-x86_64-DVD-1611.iso'
cd /root
wget -O dl.iso $url
mount -t iso9660 -o loop dl.iso /mnt
cp -r /mnt/* /var/www/iso
cp /mnt/images/pxeboot/initrd.img /var/tftpboot/pxelinux/
cp /mnt/images/pxeboot/vmlinuz /var/tftpboot/pxelinux/
umount /mnt
rm dl.iso
