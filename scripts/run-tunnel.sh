#!/bin/bash
nohup cloudflared tunnel --url http://127.0.0.1:8000 > /home/opc/litemode/tunnel.log 2>&1 &
