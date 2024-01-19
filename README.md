<div align="center">

# IP-Checker

IP-Checker is a simple application to compare the host public IP address with the DNS records of a given domain.

![Github Actions](https://github.com/chaytus/ip-checker/workflows/Tests/badge.svg)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org)
</div>

## Table of Contents
- [Why?](#why)
- [IP-Checker Program Flow](#ip-checker-program-flow)
- [Setup Python Environment](#setup-python-environment)
- [Compile and Install the Application](#compile-and-install-the-application)
- [Testing the Installation](#testing-the-installation)
- [Logging](#logging)
- [SMS Notifications](#sms-notifications)
- [Systemd Service](#systemd-service)
- [GitHub Actions and Automated Releases](#github-actions-and-automated-releases)
- [License](#license)

## Why?
I wanted an automated way to check for changes in my host public IP address.
Eventually, this will initiate a service to update the DNS records of a domain
with the new IP address. Thus saving me the cost of a static IP address, and the
hassle of keeping track of various DNS records and changing them manually.

## IP-Checker Program Flow
### Step 1: Get the public IP address of the host.
A few services are available to get the public IP address of the host. IP-Checker
expects the IP address to be `IPv4`. The following services are used to get the
public IP address:

- https://api.ipify.org
- http://www.trackip.net/ip
- http://myip.dnsomatic.com

The default service is `http://api.ipify.org`. This can be changed by setting the
environment variable `PUBLIC_IP_SERVICE` to one of the above services. Alternatively,
this can be passed as a command line argument.

```bash
ip_checker --service http://api.ipify.org
```

### Step 2: Get the IP address of the domain from the DNS records.
For a given domain, e.g. `example.com`, the DNS records can be queried to get the
IP address.

The domain can be set by setting the environment variable `DOMAIN` to the desired
domain, e.g. `example.com`. Alternatively, this can be passed as a command line
argument.

```bash
ip_checker --domain example.com
```

The default DNS servers are `1.1.1.1` and `1.0.0.1` from Cloudflare.
This can be changed by setting the environment variable `DNS_SERVERS` to a comma
separated list of DNS servers. Alternatively, one or more can be passed as a command line
argument.

```bash
ip_checker --dns-servers 1.1.1.1 ...
```

Note: IP-Checker uses the `A` record to get the IP address.


### Step 3: Compare the IP addresses.

This application can be compiled into a binary executable and run as a service.
The assumption going forward is that the host OS is Linux. Systemd is explained
below, though other init systems can be used as well.

## Setup Python Environment
This project uses [PDM](https://pdm.fming.dev/) to manage the python environment.
A virtual environment is recommended in for the following steps. After initializing
a virtual environment, install `PDM` with the following command:
```bash
pip install pdm
```

After installing `PDM`, install the dependencies with the following command:
```bash
pdm install
```

## Compile and Install the Application
After setting up the python environment with `PDM`, assemble the application with [Nuitka](https://nuitka.net/):

```bash
pdm run compile
```

This will create a binary file with the following names:
- Windows: `ip_checker.exe`
* Linux: `ip_checker.bin`
+ MacOS: `ip_checker`

Next the binary file can be copied to the desired location. For example, on Linux:
```bash
sudo cp ip_checker.bin /usr/local/bin/ip_checker
```

## Testing the Installation
The application can be run with the following command:
```bash
ip_checker
```
Without environment variables, the application will fail.
```bash
```

## Logging

TBD

## SMS Notifications
SMS notifications are sent using [Twilio](https://www.twilio.com/). The following
environment variables are required to send SMS notifications:
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_FROM_NUMBER`
- `TWILIO_TO_NUMBER`
- `TWILIO_MESSAGE`

## Systemd Service

### ip_checker.service
```bash
[Unit]
Description=Run ip-checker

[Service]
EnvironmentFile=/path/to/secure/env_file
ExecStart=/path/to/your/executable
```

### ip_checker.timer
```bash
[Unit]
Description=Run ip-checker every 5 minutes

[Timer]
OnBootSec=5min
OnUnitActiveSec=5min

[Install]
WantedBy=timers.target
```

## GitHub Actions and Automated Releases

TBD

## License

This project is open sourced under MIT license, see the [LICENSE](LICENSE) file for more details.
