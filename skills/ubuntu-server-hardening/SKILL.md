---
name: ubuntu-server-hardening
description: "Trigger: server hardening, secure ubuntu, asegurar servidor, blindar ubuntu. Automatiza la configuración de seguridad base en servidores Ubuntu."
license: Apache-2.0
metadata:
  author: "antigravity"
  version: "1.0"
---

## Activation Contract

Create or apply this skill when:
- The user needs to secure a new Ubuntu Server (headless or not).
- The user wants to apply standard hardening (SSH, Firewall, Auditing).
- Preparing a server for software installation (like ForgeOS) that requires a secure base.

## Hard Rules

- NEVER close the current SSH session while modifying network or SSH configurations until a second session confirms access.
- Use Ed25519 keys; do not use RSA keys under 3072 bits.
- SSH `PermitRootLogin` must be `no`.
- SSH `PasswordAuthentication` must be `no`.
- Firewall (UFW) must default deny incoming, allow outgoing, and explicitly allow SSH (port 22).

## Decision Gates

| Need | Action |
|------|--------|
| New SSH keys | Generate `ed25519` keys on client and `ssh-copy-id` to server |
| Firewall rules | Enable `ufw`, default deny, allow ssh |
| Brute force protection | Install and enable `fail2ban` |
| Security patches | Configure `unattended-upgrades` |

## Execution Steps

1. **SSH Hardening**:
   - Verify client has Ed25519 keys (`ssh-keygen -t ed25519`).
   - Transfer key to server (`ssh-copy-id user@server`).
   - Edit `/etc/ssh/sshd_config` to set `PermitRootLogin no`, `PasswordAuthentication no`, `PermitEmptyPasswords no`.
   - Validate sshd (`sudo sshd -t`) and restart (`sudo systemctl restart ssh`).

2. **Firewall (UFW)**:
   - Run `sudo ufw default deny incoming`.
   - Run `sudo ufw default allow outgoing`.
   - Run `sudo ufw allow ssh`.
   - Run `sudo ufw enable`.

3. **Intrusion Prevention (Fail2Ban)**:
   - Install `fail2ban` (`sudo apt install fail2ban -y`).
   - Enable and start the service (`sudo systemctl enable fail2ban && sudo systemctl start fail2ban`).

4. **Updates**:
   - Update system: `sudo apt update && sudo apt upgrade -y`.
   - Enable automatic security updates: `sudo apt install unattended-upgrades -y`.

## Output Contract

Return:
- A confirmation of the steps executed or a checklist for the user to execute.
- Warning regarding testing SSH access on a new terminal before closing the current one.
- Any ports that need to be opened manually for additional software.
