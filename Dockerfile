FROM slskd/slskd:0.22.5

RUN apt update

# Install OpenVPN
RUN apt install -y openvpn

# Install unzip
RUN apt install -y unzip

WORKDIR /etc/openvpn

RUN wget https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip && \
    unzip ovpn.zip && \
    rm ovpn.zip

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
