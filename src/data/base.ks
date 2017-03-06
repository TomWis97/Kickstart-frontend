auth --enableshadow --passalgo=sha512
# Might wanna change for manual partitioning.
autopart
text
lang en_US.UTF-8
keyboard --vckeymap=us-intl --xlayouts='us(intl)'
timezone Europe/Amsterdam
firstboot --disable
ignoredisk --only-use=sda

{net_settings}
network --hostname="{net_hostname}"

# Might wanna change for EFI booting.
bootloader --location=mbr --boot-drive=sda
eula --agreed
selinux --enforcing

install
url --url http://10.255.255.10/iso

{root_settings}
user --name="{user_name}" --gecos="{user_gecos}" --password="{user_password}" --iscrypted --groups="{user_groups}"


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
