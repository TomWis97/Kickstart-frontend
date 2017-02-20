# Kickstart-frontend
Because automating automation is awesome.

## Why this project?
I had the brilliant idea of a Docker container for deploying CentOS/RHEL VM's.

## What's the goal?
Having an Docker container with a DHCP, TFTP and kickstart server. An newly created VM PXE boots into the installation ISO. Then it requests it's kickstart file and uses it. After it's finished, you have a perfectly installed VM with stuff like it's hostname already configured.
