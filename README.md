# SLSKD mod

This repository defines a docker image based on [slskd](https://github.com/slskd/slskd) with some additions:
- OpenVPN
- ClamAV

### Required environment variables

When running the container the following environment variables must be provided:
- `OPENVPN_USER`
- `OPENVPN_PASSWD`
- `SLSKD_SLSK_USERNAME`
- `SLSKD_SLSK_PASSWORD`
- `SLSKD_DOWNLOADS_DIR`
- `SLSKD_INCOMPLETE_DIR`
- `DEST_EMAIL_ADDRESS`: Email to send the infected files notifications to.
- `ORIGIN_EMAIL_AUTHUSER`: Email that will send the notifications if ClamAV detects an infected file.
- `ORIGIN_EMAIL_AUTHPASS`: The application password for the email sending the notifications.
- `QUARANTINE_DIR`: Directory path to move the detected infected files to.

### Volumes

In order to allow OpenVPN to establish a connection the `/dev/net/tun` path must be mounted.

### Capabilities

OpenVPN also needs the `NET_ADMIN` capability to establish a connection.

### Scan integration

```yaml
integration:
  scripts:
    scan_downloaded_file:
      on:
        - DownloadDirectoryComplete
      run: /bin/sh /scan_file "dest_directory_path" $DATA
```

Note: It is important to not double quote `$DATA`.

### Run the container

```shell
sudo nerdctl run -d --name slskd -p 8080:5030 \
    -e SLSKD_SLSK_USERNAME="[REDACTED]" \
    -e SLSKD_SLSK_PASSWORD="[REDACTED]" \
    -e OPENVPN_USER="[REDACTED]" \
    -e OPENVPN_PASSWD="[REDACTED]" \
    -e DEST_EMAIL_ADDRESS="[REDACTED]" \
    -e ORIGIN_EMAIL_AUTHUSER="[REDACTED]" \
    -e ORIGIN_EMAIL_AUTHPASS="[REDACTED]" \
    -e SLSKD_NO_AUTH="true" \
    -e SLSKD_APP_DIR="/config/slskd" \
    -e SLSKD_REMOTE_CONFIGURATION="true" \
    -e QUARANTINE_DIR="/quarantine" \
    -v /dev/net/tun:/dev/net/tun \
    --cap-add=NET_ADMIN \
    msd117/slskd:latest
```
