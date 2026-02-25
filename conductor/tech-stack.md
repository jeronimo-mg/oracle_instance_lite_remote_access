# Tech Stack

## Setup and Automation
- **Bash/Shell:** Primary for low-level system configuration and environment setup.
- **Python:** For complex automation scripts and managing services.
- **Go/Rust:** Used for performance-critical CLI tools or system-level services.

## User Interface (UI)
- **noVNC:** The core web-based VNC client.
- **HTML/JS (Vanilla):** For direct and lightweight client-side interactions.
- **React (TypeScript):** Used to build a robust and type-safe management dashboard for configuring remote access.

## Deployment and Infrastructure
- **Native Linux Service:** The system is deployed directly as a native service on the Linux host (using `systemd`) to minimize overhead and ensure maximum performance.
- **Cloudflare Tunnel:** For secure, authenticated access to the web interface without exposing ports.

## Data Storage
- **SQLite:** A lightweight, serverless relational database for storing configuration, user preferences, and session metadata.
