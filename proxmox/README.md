# Proxmox VE Configuration

Proxmox VE setup for Dell OptiPlex 3060 MT with LXC containers and VMs for homelab services.

## Hardware Specifications

- **Model**: Dell OptiPlex 3060 MT
- **CPU**: Intel i3-8100T (4 cores, 3.1GHz)
- **RAM**: 16GB DDR4
- **Storage**: 512GB NVMe (OS) + 1.5TB HDD (Data)
- **Power**: ~20W idle

## Container & VM Layout

| ID | Name | Type | Purpose | Public Access | CPU | RAM | Swap | Root Disk | Mount Point |
|----|------|------|---------|---------------|-----|-----|------|-----------|-------------|
| 100 | Sandbox | CT | Samba file shares | No | 1 | 512MB | 512MB | 64GB | HDD Samba Share /docs, /photos, /media |
| 101 | Servarr | VM | Media stack (Jellyfin, *arr, qBittorrent, Navidrome, SLSKD) | Jellyfin, Jellyseerr, Music | 3 | 6GB | 2GB | 64GB | HDD Samba /media |
| 102 | pi-hole | CT | DNS ad-blocking | No | 1 | 512MB | 512MB | 6GB | - |
| 103 | Homepage | CT | Dashboard | Dash | 1 | 512MB | 512MB | 6GB | - |
| 104 | VPN | CT | Tailscale mesh VPN | No | 1 | 512MB | 512MB | 6GB | - |
| 105 | Networking | CT | Speedtest, Nginx, Cloudflare | Speedtest | 1 | 1GB | 512MB | 16GB | - |
| 106 | Cloud | VM | Nextcloud, Immich | Nextcloud, Photos | 2 | 6GB | 1GB | 16GB | HDD Samba /docs, /photos |
| 107 | Monitoring | CT | Beszel system monitoring | No | 1 | 1GB | 0GB | 32GB | - |

## Storage Layout

- **NVMe SSD (512GB)**: Proxmox OS, VM disks, container root filesystems
- **HDD (1.5TB)**: Media storage, document storage, backups
  - `/mnt/hdd/media` - Media files for Servarr VM
  - `/mnt/hdd/docs` - Document storage for Cloud VM
  - `/mnt/hdd/samba` - Samba shares for Sandbox CT

## Public Access

External access is provided via Cloudflare Tunnels (configured in Networking CT 105):

- **dash.yourdomain.com** → Homepage (CT 103)
- **jellyfin.yourdomain.com** → Jellyfin in Servarr (VM 101)
- **jellyseerr.yourdomain.com** → Jellyseerr in Servarr (VM 101)
- **music.yourdomain.com** → Navidrome in Servarr (VM 101)
- **speedtest.yourdomain.com** → Speedtest in Networking (CT 105)
- **nextcloud.yourdomain.com** → Nextcloud in Cloud (VM 106)
- **photos.yourdomain.com** → Immich in Cloud (VM 106)

## 🚀 Proxmox VE Installation

### Download and Preparation

1. Download Proxmox VE ISO from
   [official website](https://www.proxmox.com/en/downloads)
2. Create bootable USB using Rufus (Windows) or `dd` (Linux/macOS)
3. Configure BIOS settings for virtualization

### BIOS Configuration

```sh
Advanced Settings:
- Intel VT-x: Enabled
- Intel VT-d: Enabled
- Secure Boot: Disabled
- UEFI Boot: Enabled

Boot Order:
- USB Device (for installation)
- Hard Drive (after installation)
```

### Installation Steps

1. Boot from USB and select "Install Proxmox VE"
2. Accept license agreement
3. Select target disk (NVMe SSD)
4. Configure timezone and keyboard layout
5. Set root password and email
6. Configure network settings:
   - IP: YOUR_IP/24 (e.g., 192.168.1.50/24)
   - Gateway: YOUR_GATEWAY (e.g., 192.168.1.1)
   - DNS: YOUR_DNS (e.g., 192.168.1.1)

### Post-Installation Configuration

#### Update Package Sources

```bash
# Remove enterprise repository
sed -i 's/^/#/' /etc/apt/sources.list.d/pve-enterprise.list

# Add no-subscription repository
echo "deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list

# Update system
apt update && apt upgrade -y
```

#### Configure Storage

```bash
# Mount external HDD
mkdir /mnt/hdd
echo '/dev/sdb1 /mnt/hdd ext4 defaults 0 2' >> /etc/fstab
mount -a

# Create Proxmox storage for containers
pvesm add dir hdd-storage --path /mnt/hdd --content images,backup,vztmpl
```

## 📦 Container Management Strategy

### LXC vs VM Decision Matrix

| Use Case            | Container Type | Reason                                   |
| ------------------- | -------------- | ---------------------------------------- |
| Web Services        | LXC            | Lower overhead, faster deployment        |
| Media Stack         | LXC            | Better resource sharing                  |
| Databases           | LXC            | Sufficient isolation, better performance |
| Network Services    | LXC            | Easy management, quick updates           |
| Legacy Applications | VM             | Full OS isolation required               |

### Standard Container Template

```bash
# Download Ubuntu 22.04 LTS template
pveam download local ubuntu-22.04-standard_22.04-1_amd64.tar.zst

# Create container with standard settings
pct create 100 local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst \
  --hostname nextcloud \
  --memory 2048 \
  --cores 2 \
  --rootfs local-lvm:8 \
  --net0 name=eth0,bridge=vmbr0,ip=YOUR_IP/24,gw=YOUR_GATEWAY \
  --nameserver YOUR_DNS \
  --unprivileged 1 \
  --onboot 1
```

### Container Resource Allocation

| Service     | RAM (MB) | CPU Cores | Storage (GB) | IP Address    |
| ----------- | -------- | --------- | ------------ | ------------- |
| Homepage    | 512      | 1         | 8            | YOUR_IP+3 |
| Nextcloud   | 2048     | 2         | 20           | YOUR_IP |
| Pi-hole     | 512      | 1         | 8            | YOUR_IP+2 |
| Media Stack | 4096     | 4         | 50           | YOUR_IP+1 |
| Jellyfin    | 2048     | 2         | 20           | YOUR_IP+4 |
| Monitoring  | 1024     | 1         | 16           | YOUR_IP+7 |

## 🔧 Container Optimization

### Standard Post-Creation Setup

```bash
# Enter container
pct enter 100

# Update system
apt update && apt upgrade -y

# Install essential packages
apt install -y curl wget git nano htop docker.io docker-compose

# Configure Docker
systemctl enable docker
systemctl start docker
usermod -aG docker root

# Set timezone
timedatectl set-timezone YOUR_TIMEZONE
```

### Resource Monitoring

```bash
# Check container resources
pct status 100
pct config 100
pct list

# Monitor resource usage
pvestatd
```

### Backup Strategy

```bash
# Create automated backup script
cat > /root/backup-containers.sh << 'EOF'
#!/bin/bash
# Backup all containers
for ct in $(pct list | awk 'NR>1 {print $1}'); do
    vzdump $ct --storage hdd-storage --mode snapshot --compress zstd
done

# Cleanup old backups (keep 7 days)
find /mnt/hdd/dump -name "*.vma.zst" -mtime +7 -delete
EOF

chmod +x /root/backup-containers.sh

# Add to crontab (daily at 2 AM)
echo "0 2 * * * /root/backup-containers.sh" | crontab -
```

## 🌐 Network Configuration

### Firewall Rules

```bash
# Enable datacenter firewall
pve-firewall enable

# Allow SSH from local network
pve-firewall group-rule add default-in -type in -action ACCEPT -proto tcp -dport 22 -source YOUR_NETWORK/24

# Allow Tailscale mesh network
pve-firewall group-rule add default-in -type in -action ACCEPT -source 100.64.0.0/10

# Block all other external access
pve-firewall group-rule add default-in -type in -action DROP -source 0.0.0.0/0
```

### Static IP Configuration

```bash
# Configure static IP for Proxmox host
cat > /etc/network/interfaces << 'EOF'
auto lo
iface lo inet loopback

iface enp1s0 inet manual

auto vmbr0
iface vmbr0 inet static
    address YOUR_IP/24
    gateway YOUR_GATEWAY
    bridge-ports enp1s0
    bridge-stp off
    bridge-fd 0
EOF
```

## 📊 Monitoring and Maintenance

### System Health Checks

```bash
# Check system status
pveversion
pveperf
pvesm status

# Container status overview
pct list
qm list

# Storage usage
pvesm status
df -h
```

### Performance Optimization

```bash
# Optimize kernel parameters
cat >> /etc/sysctl.conf << 'EOF'
# Optimize for containers
vm.swappiness = 10
vm.vfs_cache_pressure = 50
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
EOF

sysctl -p
```

### Update Management

```bash
#!/bin/bash
# Proxmox update script
apt update
apt list --upgradable
apt upgrade -y

# Reboot if kernel updated
if [ -f /var/run/reboot-required ]; then
    echo "Reboot required. Scheduling reboot in 5 minutes..."
    shutdown -r +5
fi
```

## 🛠️ Troubleshooting

### Common Issues

**Container won't start**:

```bash
# Check container status
pct status 100
pct config 100

# View logs
journalctl -u pve-container@100
```

**Storage issues**:

```bash
# Check storage status
pvesm status
df -h /var/lib/vz
```

**Network connectivity**:

```bash
# Test container network
pct enter 100
ping 8.8.8.8
ip route show
```

**Resource constraints**:

```bash
# Monitor resource usage
htop
iotop
pvestatd
```

## 📚 Additional Resources

- [Proxmox VE Documentation](https://pve.proxmox.com/wiki/Main_Page)
- [Container Management Guide](https://pve.proxmox.com/wiki/Linux_Container)
- [Backup and Restore](https://pve.proxmox.com/wiki/Backup_and_Restore)
- [Network Configuration](https://pve.proxmox.com/wiki/Network_Configuration)

---

**Next Steps**: Once Proxmox is configured, proceed to
[Homepage Dashboard Setup](../homepage/) for service management interface.
