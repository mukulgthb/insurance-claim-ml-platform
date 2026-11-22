# Week 3: Ubuntu and Linux operations

## Environment and evidence

This exercise was reproduced on a replacement EC2 Ubuntu instance on
22 November 2026 after the previous instance was terminated.

Project directory: ~/project/insurance-claim-ml-platform

The actual OS version, Python version, storage and memory outputs are
recorded in evidence/week3-host-baseline.txt.

Dependencies were installed inside .venv using requirements-lock.txt.
python -m pip check returned: No broken requirements found.

The missing model artifact was generated using the trusted repository
script training/train.py. Uvicorn was started manually, not via systemd.

## Commands and interpretation

| Command | Purpose | Observed result / interpretation |
|---|---|---|
| whoami | Identify current user | ubuntu; application run as a non-root user |
| pwd | Identify working directory | Project checkout under ~/project |
| ls -lah | Inspect files and permissions | app, training, tests, docs and dependency manifests present |
| cat /etc/os-release | Identify OS release | Actual release captured in host-baseline evidence |
| df -h | Inspect filesystem capacity | Actual disk usage captured in host-baseline evidence |
| free -h | Inspect memory and swap | Actual memory usage captured in host-baseline evidence |
| ps aux with Uvicorn filter | Find server process | No match when stopped; PID 6860 after restart |
| ss -lntp 'sport = :8000' | Inspect TCP listener and owner | No listener when stopped; Python PID 6860 listening after restart |
| curl /health | Test local HTTP behavior | Connection refused when stopped; HTTP 200 after restart |

df -h reports filesystem storage, not RAM. free -h reports memory and
swap, not remaining disk space.

File permission output distinguishes owner, group and other-user access.
The working directory determines how relative shell paths are resolved.

## Troubleshooting reasoning

A process existing does not prove application health: it may be blocked,
not listening on the expected socket, or unable to serve valid requests.

ps checks processes. ss checks sockets and their owners. curl checks
observable HTTP behavior. These checks complement each other.

127.0.0.1 is loopback: this API is reachable locally on the instance.
0.0.0.0 binds all local IPv4 interfaces; it does not itself configure
security groups, routing or firewalls.

curl is a useful first symptom check but does not alone identify root
cause. In this incident, process and socket checks isolated a stopped
application rather than a validation problem.

No systemd service was created. systemctl status insurance-api and
journalctl -u insurance-api therefore are not evidence for this manually
launched service. Its logs are in evidence/week3-server.log.

## Access configuration

Sanitized connection pattern:
ssh -i <local-private-key.pem> ubuntu@<instance-public-address>

The actual SSH/security-group configuration must be checked separately;
the commands above do not prove which inbound rules AWS permits.
