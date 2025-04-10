from flask import Flask, render_template_string, request, jsonify, send_from_directory, Response import subprocess import os import datetime import cv2

app = Flask(name)

RECORDINGS_DIR = "/home/pi/zarn_recordings" CAMERA_INDEX = 0

HTML_TEMPLATE = """

<!DOCTYPE html><html>
<head>
    <title>ZARN Web Interface</title>
</head>
<body style="font-family: sans-serif; background-color: #111; color: #eee; padding: 20px;">
    <h2>ZARN Web Panel</h2>
    <form method="POST" action="/command">
        <input type="text" name="cmd" placeholder="Type a command..." style="width: 300px;">
        <button type="submit">Send</button>
    </form>
    <h3>Live Camera Feed</h3>
    <img src="/camera_feed" style="width: 480px; border: 2px solid #555;">
    <h3>Recent Clips</h3>
    <ul>
        {% for file in clips %}
            <li><a href="/recordings/{{file}}" style="color: lightgreen;">{{file}}</a></li>
        {% endfor %}
    </ul>
</body>
</html>
"""@app.route("/") def index(): clips = [] for root, dirs, files in os.walk(RECORDINGS_DIR): for file in sorted(files, reverse=True): if file.endswith(".mp4"): clips.append(os.path.relpath(os.path.join(root, file), RECORDINGS_DIR)) if len(clips) >= 10: break return render_template_string(HTML_TEMPLATE, clips=clips)

@app.route("/command", methods=["POST"]) def run_command(): cmd = request.form.get("cmd") try: result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode() except subprocess.CalledProcessError as e: result = e.output.decode() return f"<pre>{result}</pre><a href='/'>Back</a>"

@app.route("/recordings/path:filename") def download_clip(filename): return send_from_directory(RECORDINGS_DIR, filename, as_attachment=False)

def gen_frames(): cap = cv2.VideoCapture(CAMERA_INDEX) while True: success, frame = cap.read() if not success: break _, buffer = cv2.imencode('.jpg', frame) frame = buffer.tobytes() yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') cap.release()

@app.route('/camera_feed') def camera_feed(): return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if name == 'main': app.run(host='0.0.0.0', port=5050, debug=False)

