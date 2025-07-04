import subprocess

def run(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed

def install():
    subprocess.run("pip install requests edge_tts ffmpeg-python matplotlib")
    exit(0)