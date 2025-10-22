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

./start.sh
