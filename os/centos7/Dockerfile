FROM tomwis97/kickstart-frontend

RUN mkdir /var/tftpboot/pxelinux
COPY pxelinux /var/tftpboot/pxelinux
COPY pickurl.py /tmp/pickurl.py
COPY setup.sh /tmp/setup.sh
RUN cd /tmp && chmod +x setup.sh && ./setup.sh
