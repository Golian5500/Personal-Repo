import os
import subprocess
import threading
import time
import cv2
import imageio_ffmpeg
import numpy as np
from flask import Flask, jsonify, render_template_string, send_file
import mss

app = Flask(__name__)
os.makedirs('static', exist_ok=True)

status = {"ready": None}
LATEST_FRAME = None  # Global to store the latest raw image for debugging

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Buffered 10s Screen Stream</title>
    <style>
        body { margin: 0; background-color: #111; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; font-family: sans-serif; }
        .container { text-align: center; width: 100%; max-width: 1280px; }
        video { width: 100%; aspect-ratio: 16/9; background: #000; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        #status-text { color: #888; margin-top: 10px; }
        a { color: #007bff; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <video id="player" autoplay muted playsinline></video>
        <div id="status-text">Waiting for the first 10-second recording...</div>
        <p style="color: #555; font-size: 12px;">Black screen? Check the <a href="/debug" target="_blank">/debug view</a></p>
    </div>
    <script>
        const player = document.getElementById('player');
        const statusText = document.getElementById('status-text');
        let currentFileLetter = '';

        function checkAndPlayNextChunk() {
            fetch('/current_chunk')
                .then(response => response.json())
                .then(data => {
                    if (data.ready && data.ready !== currentFileLetter) {
                        currentFileLetter = data.ready;
                        statusText.innerText = "Playing chunk: " + currentFileLetter;
                        player.src = `/static/stream${currentFileLetter}.mp4?t=` + new Date().getTime();
                        player.play().catch(e => console.log("Playback interaction trigger needed."));
                    }
                });
        }
        player.onended = () => { checkAndPlayNextChunk(); };
        const startupCheck = setInterval(() => {
            fetch('/current_chunk').then(response => response.json()).then(data => {
                if (data.ready) { clearInterval(startupCheck); checkAndPlayNextChunk(); }
            });
        }, 2000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/current_chunk')
def current_chunk():
    return jsonify(status)

# A diagnostic route to see exactly what Python sees
@app.route('/debug')
def debug_view():
    global LATEST_FRAME
    if LATEST_FRAME is not None:
        _, img_encoded = cv2.imencode('.jpg', LATEST_FRAME)
        return send_file(cv2.io.BytesIO(img_encoded.tobytes()), mimetype='image/jpeg')
    return "No frame captured yet. Wait 10 seconds and refresh."

def video_recording_loop():
    global status, LATEST_FRAME
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    with mss.mss() as sct:
        # Step 1: Detect which monitor index actually has an active display image
        monitor_index = 1
        if len(sct.monitors) > 1:
            for idx in range(1, len(sct.monitors)):
                test_shot = sct.grab(sct.monitors[idx])
                test_arr = np.array(test_shot)
                # Check if the screen contains anything other than pure black pixels
                if np.any(test_arr > 0):
                    monitor_index = idx
                    print(f"[MONITOR] Found active display on Monitor index: {monitor_index}")
                    break
            else:
                print("[WARNING] All separate monitors returned black. Defaulting to index 0 (Combined Desktop).")
                monitor_index = 0
        
        monitor = sct.monitors[monitor_index]
        test_shot = sct.grab(monitor)
        raw_h, raw_w, _ = np.array(test_shot).shape
        width = (raw_w // 2) * 2
        height = (raw_h // 2) * 2
        
        current_buffer = 'A'
        
        while True:
            filename = f"static/stream{current_buffer}.mp4"
            
            ffmpeg_cmd = [
                ffmpeg_exe, '-y',
                '-f', 'rawvideo', '-vcodec', 'rawvideo', '-pix_fmt', 'bgr24',
                '-s', f'{width}x{height}', '-r', '30', '-i', '-', 
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                '-preset', 'ultrafast', '-tune', 'zerolatency',
                '-movflags', '+faststart', '-t', '10',
                filename
            ]
            
            process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            start_time = time.time()
            while time.time() - start_time < 10.0:
                frame_start = time.time()
                
                screenshot = sct.grab(monitor)
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                frame = cv2.resize(frame, (width, height))
                
                # Expose this frame to the /debug endpoint
                LATEST_FRAME = frame.copy()
                
                try:
                    process.stdin.write(frame.tobytes())
                except Exception:
                    break
                
                elapsed = time.time() - frame_start
                if elapsed < 0.033:
                    time.sleep(0.033 - elapsed)
            
            try:
                process.stdin.close()
            except Exception:
                pass
            process.wait()
            
            status["ready"] = current_buffer
            print(f"[SAVED] Chunk {current_buffer} successfully exported.")
            current_buffer = 'B' if current_buffer == 'A' else 'A'

if __name__ == '__main__':
    recorder = threading.Thread(target=video_recording_loop, daemon=True)
    recorder.start()
    app.run(host='0.0.0.0', port=5000, threaded=True)