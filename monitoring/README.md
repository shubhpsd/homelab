# Monitoring Setup

Monitor your entire homelab infrastructure with Beszel - a lightweight, self-hosted monitoring solution that provides real-time insights into system performance across all your Proxmox containers and VMs.

![Beszel Dashboard](beszel%201.png)
![System Metrics](beszel%202.png)

## Services Included

- **Beszel Hub**: Central monitoring dashboard and data collector (runs in LXC 107)
- **Beszel Agents**: Lightweight monitoring agents installed on each system you want to monitor

## Architecture Overview

```text
Beszel Hub (LXC 107) ← Collects data from → Beszel Agents (on each monitored system)
     ↓
Web Dashboard (Port 8090)
```

## Installation Methods

### Step 1: Install Beszel Hub (Central Server)

The Beszel Hub is the central monitoring dashboard that collects data from all your agents. Install this once on your Proxmox host using the community script:

```bash
bash -c "$(wget -qLO - https://github.com/tteck/Proxmox/raw/main/ct/beszel.sh)"
```

This script will:

- Create LXC container 107 for Beszel Hub
- Install and configure the Beszel server
- Set up the web interface on port 8090
- Generate SSH keys for agent authentication

After installation, access the hub at `http://YOUR_PROXMOX_IP:8090` to complete setup.

### Step 2: Install Beszel Agents (On Systems to Monitor)

Install agents on each system you want to monitor. Choose the method that works best for each target system:

#### Method A: Docker Compose Agent (Recommended for Docker hosts)

For systems already running Docker (VMs, other servers):

```bash
# Clone the repository and navigate to monitoring
cd monitoring

# Copy and configure environment variables
cp .env.example .env
nano .env

# Start the Beszel agent
docker-compose up -d
```

#### Method B: Binary Agent Installation

For LXC containers, bare metal systems, or anywhere Docker isn't available:

```bash
# Download the latest Beszel agent binary
curl -sL "https://github.com/henrygd/beszel/releases/latest/download/beszel-agent_$(uname -s)_$(uname -m | sed 's/x86_64/amd64/').tar.gz" | tar -xz -O beszel-agent | sudo tee /usr/local/bin/beszel-agent > /dev/null && sudo chmod +x /usr/local/bin/beszel-agent

# Create systemd service
sudo tee /etc/systemd/system/beszel-agent.service > /dev/null <<EOF
[Unit]
Description=Beszel Agent
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/beszel-agent -k "YOUR_SSH_PUBLIC_KEY" -t "YOUR_AGENT_TOKEN" -p 45876 "YOUR_HUB_URL"
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable beszel-agent
sudo systemctl start beszel-agent
```

## Configuration

### Setting Up the Hub (LXC 107)

1. Access the Beszel Hub web interface at `http://YOUR_PROXMOX_IP:8090`
2. Complete the initial setup wizard
3. Create admin credentials
4. The hub will generate SSH keys and tokens for agent authentication

### Adding Agents to Monitor Systems

For each system you want to monitor:

1. In the Beszel Hub interface, go to "Systems"
2. Click "Add System" to generate:
   - SSH public key
   - Agent token
   - Connection details

3. Use these credentials to configure the agent on your target system

### Typical Deployment in Your Homelab

- **Beszel Hub**: Running in LXC 107 (installed via Proxmox script)
- **Agents to install**:
  - Proxmox host itself (binary installation)
  - LXC 100 (Samba) - binary installation
  - LXC 102 (Pi-hole) - binary installation
  - LXC 103 (Homepage) - Docker agent
  - LXC 104 (Tailscale) - binary installation
  - LXC 105 (Networking) - Docker agent
  - VM 101 (Media stack) - Docker agent
  - VM 106 (Cloud services) - Docker agent

### Environment Variables

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Configure the following variables:

- `BESZEL_HUB_URL`: Your Beszel Hub URL (e.g., `http://YOUR_HUB_IP:8090`)
- `BESZEL_AGENT_KEY`: SSH public key from the hub
- `BESZEL_AGENT_TOKEN`: Agent token from the hub

## Monitoring Your Homelab

Once the hub is set up and agents are installed, Beszel will monitor:

1. **Proxmox Host**: Physical server metrics (via binary agent)
2. **LXC Containers**: Individual container performance
   - LXC 100 (Samba) - binary agent
   - LXC 102 (Pi-hole) - binary agent  
   - LXC 103 (Homepage) - Docker agent
   - LXC 104 (Tailscale) - binary agent
   - LXC 105 (Networking) - Docker agent
   - LXC 107 (Beszel Hub) - monitored by hub itself
3. **Virtual Machines**: VM resource usage
   - VM 101 (Media stack) - Docker agent
   - VM 106 (Cloud services) - Docker agent

## Troubleshooting

### Agent Connection Issues

Check agent logs:

```bash
# Docker
docker-compose logs beszel-agent

# Systemd service
sudo journalctl -u beszel-agent -f
```

### Firewall Configuration

Ensure port 45876 is open for agent communication:

```bash
# UFW
sudo ufw allow 45876

# iptables
sudo iptables -A INPUT -p tcp --dport 45876 -j ACCEPT
```

### Hub Access Issues

1. Verify the hub is running on port 8090
2. Check firewall rules for port 8090
3. Ensure the hub URL is accessible from agent systems

## Resources

- [Beszel GitHub Repository](https://github.com/henrygd/beszel)
- [Proxmox Community Scripts](https://github.com/tteck/Proxmox)
- [Official Documentation](https://github.com/henrygd/beszel#readme)

## Integration with Other Services

Beszel complements your existing monitoring setup:

- Works alongside Proxmox's built-in monitoring
- Provides detailed insights for Docker services
- Can monitor services running in containers like Homepage, Pi-hole, etc.
- Lightweight enough to run on resource-constrained systems
