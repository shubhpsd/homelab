# My Homelab Setup

Self-hosted services running on Proxmox VE with Dell OptiPlex 3060 MT. This repository contains Docker Compose files, configurations, and documentation for replicating my homelab setup.

## Quick Start

### Clone Specific Services

You don't need to clone the entire repository! Use these commands to download only the services you want:

```bash
# Clone just the media stack
git clone --filter=blob:none --sparse https://github.com/shubhpsd/homelab.git
cd homelab
git sparse-checkout set media

# Or clone multiple specific folders
git clone --filter=blob:none --sparse https://github.com/shubhpsd/homelab.git
cd homelab
git sparse-checkout set cloud networking monitoring

# Or clone everything (full repository)
git clone https://github.com/shubhpsd/homelab.git
```

Available folders: `proxmox`, `homepage`, `samba`, `cloud`, `media`, `networking`, `monitoring`, `apps`

## Navigation

- [Glance Dashboard](./homepage/) - Service dashboard and monitoring
- [Cloud Storage](./cloud/) - Nextcloud and Immich running in VMs
- [Media Server](./media/) - Jellyfin, \*arr stack, Navidrome, and more
- [Server Monitoring](./monitoring/) - Beszel monitoring and system metrics
- [Proxy Management](./networking/) - Nginx Proxy Manager and Cloudflare Tunnels
- [Samba Storage](./samba/) - Network file shares
- [Proxmox Setup](./proxmox/) - Virtualization platform configuration

## Hardware

![Dell OptiPlex 3060 MT](./proxmox/server.jpg)

### Server Specifications

#### Dell OptiPlex 3060 MT (Proxmox VE)

- Intel i3-8100T (4 cores, 3.1GHz)
- 16GB DDR4 RAM
- 512GB NVMe SSD (Proxmox OS + VM disks)
- 1.5TB HDD (Media, Documents, Backups)
- ~20W idle power consumption
- Gigabit Ethernet

## Service Overview

### Containers (LXC)

| ID  | Name       | Purpose                      | CPU | RAM   | Storage |
| --- | ---------- | ---------------------------- | --- | ----- | ------- |
| 100 | Sandbox    | Samba file shares            | 1   | 512MB | 64GB    |
| 102 | Pi-hole    | DNS ad-blocking              | 1   | 512MB | 6GB     |
| 103 | Homepage   | Service dashboard            | 1   | 512MB | 6GB     |
| 104 | VPN        | Tailscale mesh network       | 1   | 512MB | 6GB     |
| 105 | Networking | Nginx, Cloudflare, Speedtest | 1   | 1GB   | 16GB    |
| 107 | Monitoring | Beszel system monitoring     | 1   | 1GB   | 32GB    |

### Virtual Machines

| ID  | Name    | Purpose                             | CPU | RAM | Storage |
| --- | ------- | ----------------------------------- | --- | --- | ------- |
| 101 | Servarr | Media stack (Jellyfin, \*arr, etc.) | 3   | 6GB | 64GB    |
| 106 | Cloud   | Nextcloud + Immich                  | 2   | 6GB | 32GB    |

## External Access

All services accessible via Cloudflare Tunnels at `*.yourdomain.com`:

### Public Services

- **dash.yourdomain.com** → Glance Dashboard
- **jellyfin.yourdomain.com** → Jellyfin Media Server
- **jellyseerr.yourdomain.com** → Media Requests
- **music.yourdomain.com** → Navidrome Music Streaming
- **nextcloud.yourdomain.com** → Personal Cloud Storage
- **photos.yourdomain.com** → Immich Photo Management
- **speedtest.yourdomain.com** → Network Speed Testing

### Internal Only

- Pi-hole DNS (YOUR_NETWORK)
- Proxmox Web Interface
- Samba File Shares
- Monitoring Dashboards
