FROM slskd/slskd:0.24.0

RUN apt update

# Install clamav
RUN apt install clamav clamav-daemon -y

# Install ssmtp and mailutils
RUN apt install ssmtp mailutils -y

# Install python3
RUN apt install python3 -y

COPY files/scan_file.py /scan_file.py
RUN chmod +x /scan_file.py

COPY files/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /slskd

ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]
