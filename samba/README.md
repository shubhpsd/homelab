
# Samba Shares: Storage Pooling & VM Access

![Samba share demo](./samba-share.gif)

This guide documents the setup for using Samba shares as a storage pool accessible by VMs and containers in a homelab environment.

## 1. Samba Server Setup (LXC Container)

[**Example: `/etc/samba/smb.conf`**]

```ini
[Photos]
    path = /mnt/hdd/Photos
    browsable = yes
    writable = yes
    guest ok = no
    read only = no
```

**LXC Mount Example: `/etc/pve/lxc/100.conf`**

```ini
[global]
    workgroup = WORKGROUP
    server string = Samba Server
    security = user
    map to guest = Bad User
    dns proxy = no
    # Add more global options as needed

[Media]
    path = /mnt/hdd/Media
    browsable = yes
    writable = yes
    guest ok = no
    read only = no

[Documents]
    path = /mnt/hdd/Documents
    browsable = yes
    writable = yes
    guest ok = no
    read only = no

[Photos]
    path = /mnt/hdd/Photos
    browsable = yes
    writable = yes
    guest ok = no
    read only = no
```

**LXC Mount Example: `/etc/pve/lxc/100.conf`**

```ini

mp0: /mnt/pve/hdd,mp=/mnt/hdd
```

This mounts the Proxmox storage pool into the Samba LXC at `/mnt/hdd`.

---

## 2. VM Configuration (Proxmox)

**Example: `/etc/pve/qemu-server/101.conf` (Servarr/media VM)**

```ini
name: servarr
scsi0: local-lvm:vm-101-disk-0,iothread=1,size=64G
# ...other config...
```

**Example: `/etc/pve/qemu-server/106.conf` (Cloud/Nextcloud/Immich VM)**

```ini
name: cloud
scsi0: local-lvm:vm-106-disk-0,iothread=1,size=32G
# ...other config...
```

---

## 3. Mounting Samba Shares in VMs

**Inside each VM, add entries to `/etc/fstab` to mount the shares at boot:**

### Servarr VM (`/etc/fstab`)

```ini
//<SAMBA_SERVER_IP>/Media  /data   cifs credentials=/etc/cifs-creds,uid=1000,gid=1000,iocharset=utf8 0 0
```

### Cloud VM (`/etc/fstab`)

```ini
//<SAMBA_SERVER_IP>/Documents /docs   cifs credentials=/etc/cifs-creds,uid=1000,gid=1000,iocharset=utf8,file_mode=0770,dir_mode=0770,noperm 0 0
//<SAMBA_SERVER_IP>/Photos    /photos cifs credentials=/etc/cifs-creds,uid=1000,gid=1000,iocharset=utf8,file_mode=0770,dir_mode=0770,noperm 0 0
```

**Credentials file example (`/etc/cifs-creds`):**

```ini
username=your_samba_user
password=your_samba_password
```

Set permissions: `chmod 600 /etc/cifs-creds`

---

## 4. Mounting and Troubleshooting

- After editing `/etc/fstab`, run `sudo mount -a` to mount all shares.
- Ensure the Samba user exists and has access to the shared folders.
- Use `testparm` to validate your `smb.conf`.
- Check permissions on the host storage directory (e.g., `/mnt/hdd/Media`).

---

## 5. Diagram

```text
Proxmox Host
 ├─ LXC: samba (shares /mnt/hdd/*)
 │    └─ [Media, Documents, Photos]
 ├─ VM: servarr (mounts //<SAMBA_SERVER_IP>/Media → /data)
 └─ VM: cloud (mounts //<SAMBA_SERVER_IP>/Documents → /docs, //<SAMBA_SERVER_IP>/Photos → /photos)
```

---

## 6. Template Notes

- Replace `<SAMBA_SERVER_IP>` with your Samba server's IP address.
- Adjust share names and mount points as needed.
- Use this as a template for any VM/container needing access to shared storage.

---

**This setup enables centralized storage pooling and easy access for all your homelab services.**
