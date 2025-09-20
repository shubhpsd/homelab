# Homepage Dashboard

Homepage is a modern, aesthitically pleasing, highly customizable application dashboard with integrations for over 100 services.

![Homepage Dashboard](homepage-dashboard.png)

## External Access

The following services are configured with public access through Cloudflare Tunnels and Nginx Proxy Manager (see [networking folder](../networking/) for setup):

- **<https://dash.yourdomain.com>** → Homepage Dashboard
- **<https://jellyfin.yourdomain.com>** → Jellyfin Media Server
- **<https://jellyseerr.yourdomain.com>** → Media Request Management
- **<https://music.yourdomain.com>** → Navidrome Music Streaming
- **<https://nextcloud.yourdomain.com>** → Personal Cloud Storage
- **<https://photos.yourdomain.com>** → Immich Photo Management
- **<https://speedtest.yourdomain.com>** → Network Speed Testing

All other services (Proxmox, *arr stack, download clients, etc.) remain internal-only for security.

## Setup Instructions

1. **Copy environment file**:

   ```bash
   cp docker.env.example docker.env
   ```

2. **Edit environment variables** with your API keys and credentials:

   ```bash
   nano docker.env
   ```

3. **Configure IP addresses** in `config/services.yaml`:
   - Replace `YOUR_PROXMOX_IP` with your Proxmox server IP
   - Replace `YOUR_MEDIA_SERVER_IP` with your media VM/container IP  
   - Replace `YOUR_BESZEL_IP` with your monitoring container IP
   - Replace `YOUR_PIHOLE_IP` with your Pi-hole container IP
   - Replace `YOUR_NPM_IP` with your Nginx Proxy Manager IP
   - Replace `YOUR_SAMBA_IP` with your Samba file server IP

4. **Customize personal settings**:
   - Update `config/settings.yaml` with your homelab name and preferences
   - Update `config/widgets.yaml` with your location coordinates
   - Update `config/bookmarks.yaml` with your personal links

5. **Deploy with Docker Compose**:

   ```bash
   docker-compose up -d
   ```

6. **Access the dashboard** at `http://localhost:3000` or your configured domain

## Configuration Files

- **`compose.yaml`** - Docker Compose configuration
- **`docker.env`** - Environment variables and API keys
- **`config/services.yaml`** - Service definitions and widgets
- **`config/settings.yaml`** - Dashboard theme and layout settings
- **`config/widgets.yaml`** - System widgets configuration
- **`config/bookmarks.yaml`** - Bookmark definitions
- **`config/docker.yaml`** - Docker integration settings
- **`config/proxmox.yaml`** - Proxmox monitoring configuration

## Customization

### Adding New Services

Edit `config/services.yaml` to add new services to the dashboard. Follow the existing format and check [Homepage documentation](https://gethomepage.dev/configs/services/) for widget types.

### Changing Theme

Modify `config/settings.yaml` to change:

- Background image and effects
- Color theme (dark/light)
- Layout and columns
- Page title and header

### Widget Configuration

Update `config/widgets.yaml` to customize:

- System resource monitoring
- Weather widget location
- Custom logo

## API Keys Required

You'll need to obtain API keys for the following services:

- Radarr, Sonarr, Lidarr, Bazarr (Settings → General → API Key)
- Jellyfin (Dashboard → API Keys)
- Jellyseerr (Settings → General → API Key)
- Tailscale (Admin Console → Settings → Keys)
- Immich (Account Settings → API Keys)
- Nextcloud (Personal Settings → Security → App passwords)
- Cloudflare (My Profile → API Tokens)

## Notes

- All sensitive credentials are stored in environment variables
- The dashboard uses read-only access where possible
- Docker socket is mounted for container monitoring
- External storage is mounted read-only for disk usage monitoring

## Troubleshooting

### Widget Not Loading

1. Check API key is correct in `docker.env`
2. Verify service URL is accessible from container
3. Check Homepage logs: `docker logs homepage`

### Service Not Responding

1. Verify service is running and accessible
2. Check network connectivity between containers
3. Validate API endpoint URLs in `services.yaml`

For more configuration options, see the [official Homepage documentation](https://gethomepage.dev/).
