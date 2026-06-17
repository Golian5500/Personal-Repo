import subprocess
import os

# 1. Ensure ffmpeg is installed and in your PATH
# 2. This command captures the desktop, encodes it efficiently, 
#    and serves it as a local stream.
command = [
    'ffmpeg',
    '-f', 'gdigrab',          # Windows screen capture
    '-framerate', '30',       # Stable 30fps
    '-i', 'desktop',          # Capture the full desktop
    '-c:v', 'libx264',        # High-performance encoding
    '-preset', 'ultrafast',   # Lower CPU usage
    '-tune', 'zerolatency',   # Minimal lag
    '-f', 'mpegts',           # Streaming format
    'udp://0.0.0.0:12345'     # Stream to all network devices
]

# Run the stream
process = subprocess.Popen(command)

print("Stream is live! Open the stream on your TV/Phone using VLC: udp://@:12345")