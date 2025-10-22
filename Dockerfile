FROM slskd/slskd:0.23.2

RUN apt update

# Install clamav
RUN apt install clamav clamav-daemon -y

# Install ssmtp and mailutils
RUN apt install ssmtp mailutils -y

COPY files/scan_file /scan_file
RUN chmod +x /scan_file

COPY files/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /slskd

ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]
