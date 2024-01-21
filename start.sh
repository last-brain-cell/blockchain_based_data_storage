#!/bin/bash

python peer.py &

python run_app.py

# Keep the container running
tail -f /dev/null
