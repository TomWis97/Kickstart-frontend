FROM tomwis97/kickstart-frontend:latest

RUN mkdir /var/tftpboot/pxelinux
COPY pxelinux /var/tftpboot/pxelinux
COPY pickurl.py /tmp/pickurl.py
COPY setup.sh /tmp/setup.sh
RUN cd /tmp && python3 pickurl.py
RUN cd /tmp && chmod +x setup.sh && ./setup.sh
