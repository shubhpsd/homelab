# Homelab Service Gallery

This page showcases all the applications and services running in this homelab setup. Each service includes a screenshot and links to detailed configuration guides in their respective directories.

## Quick Navigation

- [📊 **Proxmox**](../proxmox/) - Virtualization platform and infrastructure setup
- [🏠 **Homepage**](../homepage/) - Service dashboard and monitoring
- [📁 **Samba**](../samba/) - Network file sharing and storage
- [☁️ **Cloud Services**](../cloud/) - Nextcloud and Immich for file storage and photo backup
- [🎬 **Media Stack**](../media/) - Complete entertainment and media management
- [🌐 **Networking**](../networking/) - DNS, proxy, and network infrastructure
- [📈 **Monitoring**](../monitoring/) - System monitoring and observability

---

## Service Overview

### Infrastructure & Management

#### Homepage Dashboard
![Homepage Dashboard](../homepage/homepage-dashboard.png)

**Purpose:** Central dashboard for accessing all services  
**Details:** [Homepage Configuration](../homepage/)

---

### Storage & Files

#### Nextcloud
![Nextcloud](../cloud/nextcloud.png)

**Purpose:** Self-hosted cloud storage and collaboration  
**Details:** [Cloud Services Setup](../cloud/)

#### Immich
![Immich](../cloud/immich.png)

**Purpose:** Photo backup and management (Google Photos replacement)  
**Details:** [Cloud Services Setup](../cloud/)

#### Samba File Server
![Samba Demo](../samba/samba-share.gif)

**Purpose:** Network file sharing and centralized storage  
**Details:** [Samba Configuration](../samba/)

---

### Media & Entertainment

#### Jellyfin
![Jellyfin](../media/images/jellyfin.png)

**Purpose:** Open-source media streaming server  
**Details:** [Media Stack Setup](../media/)

#### Jellyseerr
![Jellyseerr](../media/images/jellyseerr.png)

**Purpose:** Media request and discovery platform  
**Details:** [Media Stack Setup](../media/)

#### Radarr
![Radarr](../media/images/radarr.png)

**Purpose:** Movie collection management  
**Details:** [Media Stack Setup](../media/)

#### Sonarr
![Sonarr](../media/images/sonarr.png)

**Purpose:** TV series collection management  
**Details:** [Media Stack Setup](../media/)

#### Lidarr
![Lidarr](../media/images/lidarr.png)

**Purpose:** Music collection management  
**Details:** [Media Stack Setup](../media/)

#### Bazarr
![Bazarr](../media/images/bazarr.png)

**Purpose:** Subtitle management for movies and TV shows  
**Details:** [Media Stack Setup](../media/)

#### qBittorrent
![qBittorrent](../media/images/qbittorrent.png)

**Purpose:** BitTorrent client for downloading content  
**Details:** [Media Stack Setup](../media/)

#### Navidrome
![Navidrome](../media/images/navidrome.png)

**Purpose:** Music streaming server and web player  
**Details:** [Media Stack Setup](../media/)

#### SoulSeek (slskd)
![SoulSeek](../media/images/slskd.png)

**Purpose:** Peer-to-peer music sharing network client  
**Details:** [Media Stack Setup](../media/)

#### JellyStat
![JellyStat](../media/images/jellystat.png)

**Purpose:** Jellyfin statistics and analytics  
**Details:** [Media Stack Setup](../media/)

---

### Networking & Security

#### Pi-hole
![Pi-hole Dashboard](../networking/pihole-dashboard.png)

**Purpose:** Network-wide ad blocking and DNS management  
**Details:** [Networking Setup](../networking/)

#### Speedtest
![Speedtest](../networking/speedtest.png)

**Purpose:** Network speed monitoring and testing  
**Details:** [Networking Setup](../networking/)

---

### Monitoring & Analytics

#### Beszel
![Beszel Dashboard](../monitoring/beszel%201.png)

**Purpose:** Lightweight system monitoring and observability  
**Details:** [Monitoring Setup](../monitoring/)

---

## Getting Started

1. **Start with Infrastructure:** Set up [Proxmox](../proxmox/) as your virtualization platform
2. **Configure Networking:** Set up [Pi-hole and NGINX Proxy Manager](../networking/)
3. **Deploy Services:** Choose services based on your needs:
   - **Essential:** Homepage dashboard, Samba file sharing
   - **Media:** Complete media stack with *arr applications
   - **Cloud:** Nextcloud for files, Immich for photos
   - **Monitoring:** Beszel for system insights

## Service Distribution

- **LXC Containers:** Lightweight services (Pi-hole, Homepage, Samba, Tailscale, Beszel)
- **Virtual Machines:** Resource-intensive applications (Media stack, Cloud services)
- **Docker Compose:** Easy deployment and management of multi-container applications

Each service directory contains:
- Complete Docker Compose configurations
- Environment variable templates
- Setup instructions and screenshots
- Integration guides with other services