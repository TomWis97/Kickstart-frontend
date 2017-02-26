auth --enableshadow --passalgo=sha512
# Might wanna change for manual partitioning.
autopart
text
lang en_US.UTF-8
keyboard --vckeymap=us-intl --xlayouts='us(intl)'
timezone Europe/Amsterdam
firstboot --disable
ignoredisk --only-use=sda

#network --bootproto=dhcp --activate --device=link
network --bootproto=static --ip={net-ip} --netmask={net-netmask} --gateway={net-gateway} --nameserver={net-nameserver} --device=link
network --hostname={net-hostname}

# Might wanna change for EFI booting.
bootloader --location=mbr --boot-drive=sda
eula --agreed
selinux --enforcing

install
url --url http://server/path

rootpw --iscrypted {root-password}
user --name={user-name} --gecos={user-gecos} --iscrypted={user-password} --groups=wheel


# Maybe interesting options:
# - firewall
# - clearparts
# - firstboot
# - group (create groups)
# - halt, poweroff, reboot of shutdown.
# - partition
# - repo
# - services
# - sshpw
# - zerombr
# - %packages
# - %pre
# - %post
# Documentation: https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Installation_Guide/sect-kickstart-syntax.html