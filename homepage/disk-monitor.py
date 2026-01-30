#!/usr/bin/env python3
"""
Simple HTTP server that provides disk usage information for Glance extension widget.
Monitors mounted storage and returns HTML with progress bars.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import shutil


class DiskMonitorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/disk-status":
            # Get disk usage for the mounted volume
            # For macOS: /Volumes/Docs (SMB share: //homelab/Docs)
            # For LXC: /mnt/hdd500
            paths = [
                # {"title": "Root Filesystem", "path": "/mnt/root"},
                {"title": "HDD Storage (1.4TB)", "path": "/mnt/hdd500"},
            ]

            html_parts = []

            for disk in paths:
                try:
                    if not os.path.exists(disk["path"]):
                        continue

                    usage = shutil.disk_usage(disk["path"])
                    total_gb = usage.total / (1024**3)
                    used_gb = usage.used / (1024**3)
                    free_gb = usage.free / (1024**3)
                    percent = (usage.used / usage.total) * 100

                    # Determine color based on usage: <=60% green, 60-80% yellow, >80% red
                    if percent > 80:
                        color_class = "negative"
                        bar_color = "#fb4934"  # gruvbox red
                    elif percent > 60:
                        color_class = "notice"
                        bar_color = "#fe8019"  # gruvbox orange
                    else:
                        color_class = "positive"
                        bar_color = "#b8bb26"  # gruvbox green

                    html = f"""
<div class="server margin-bottom-10">
  <div class="server-info">
    <div class="server-details">
      <div class="server-name color-highlight size-h3 text-truncate">
        {disk["title"]}
      </div>
      <div class="size-h5">{disk["path"]}</div>
    </div>
  </div>
  <div class="server-stats">
    <div class="flex-1">
      <div class="size-h5 text-center">
        <div class="color-base">USED</div>
        <div class="color-highlight">{used_gb:.1f} GB</div>
      </div>
    </div>
    <div class="flex-1">
      <div class="size-h5 text-center">
        <div class="color-base">FREE</div>
        <div class="color-highlight">{free_gb:.1f} GB</div>
      </div>
    </div>
    <div class="flex-1">
      <div class="size-h5 text-center">
        <div class="color-base">TOTAL</div>
        <div class="color-highlight">{total_gb:.1f} GB</div>
      </div>
    </div>
  </div>
</div>
<div class="flex justify-between items-end size-h5 margin-top-10">
  <div>STORAGE</div>
  <div class="color-{color_class} text-very-compact">
    <span>{percent:.1f}</span> <span class="color-base">%</span>
  </div>
</div>
<div class="progress-bar progress-bar-combined">
  <div class="progress-value" style="--percent: {percent:.1f}; background: {bar_color};"></div>
</div>
"""
                    html_parts.append(html)
                except Exception as e:
                    html_parts.append(
                        f'<div class="size-h5 color-negative">Error reading {disk["path"]}: {str(e)}</div>'
                    )

            final_html = (
                "\n".join(html_parts)
                if html_parts
                else '<div class="size-h5 color-negative">No mounted storage found</div>'
            )

            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Widget-Content-Type", "html")
            self.send_header("Widget-Title", "External Storage")
            self.end_headers()
            self.wfile.write(final_html.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress default logging
        pass


def run_server(port=8888):
    server = HTTPServer(("0.0.0.0", port), DiskMonitorHandler)
    print(f"Disk monitor server running on port {port}...")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
