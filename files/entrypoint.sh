#!/bin/sh

# Configure mailutils
cat > /etc/ssmtp/ssmtp.conf << EOF
root=postmaster
SERVER=${ORIGIN_EMAIL_AUTHUSER}

mailhub=smtp.gmail.com:587
AuthUser=${ORIGIN_EMAIL_AUTHUSER}
Authpass=${ORIGIN_EMAIL_AUTHPASS}
UseTLS=YES
UseSTARTTLS=YES

FromLineOverride=YES
EOF

# Update the virus database
freshclam

# Create auth file
echo "${OPENVPN_USER}" > /etc/openvpn/auth.txt
echo "${OPENVPN_PASSWD}" >> /etc/openvpn/auth.txt

openvpn \
    --config /etc/openvpn/ovpn_udp/es114.nordvpn.com.udp.ovpn \
    --auth-user-pass /etc/openvpn/auth.txt &

./start.sh
