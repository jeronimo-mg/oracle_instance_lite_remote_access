# Tech Stack

## Setup and Automation
- **Bash/Shell:** Primary for low-level system configuration and environment setup.
- **Python (FastAPI):** For complex automation scripts, managing services, and providing the backend API for the dashboard.
- **Go/Rust:** Used for performance-critical CLI tools or system-level services.


## User Interface (UI)
- **Wayland (Weston):** The core compositor for the remote desktop. Uses `weston-vnc` for remote access.
- **noVNC:** The core web-based VNC client.
- **HTML/JS (Vanilla):** For direct and lightweight client-side interactions.
- **React (TypeScript):** Used to build a robust and type-safe management dashboard for configuring remote access.

## Deployment and Infrastructure
- **Native Linux Service:** The system is deployed directly as a native service on the Linux host (using `systemd`) to minimize overhead and ensure maximum performance.
- **Tailscale:** For secure, private access to the web interface and VNC without exposing ports to the public internet. Provides a stable "MagicDNS" name.

## Data Storage
- **SQLite:** A lightweight, serverless relational database for storing configuration, user preferences, and session metadata.

---

### Deviations and Design Decisions
- **2026-02-25:** Replaced XFCE/x11vnc with Weston (Wayland) because XFCE and x11vnc are not available in standard Oracle Linux 10.1 repositories.
- **2026-02-25:** Replaced Cloudflare Tunnel with Tailscale. Tailscale provides a stable, secure, and free way to access the instance without requiring a public domain name, which aligns better with the "lite-mode" for personal use.


