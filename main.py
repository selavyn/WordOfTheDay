import sys
import subprocess
import os
import asyncio
import json
from setup import run
import setup
try:
    import requests
    import edge_tts
    import ffmpeg
    import matplotlib.font_manager
except ImportError as e:
    if sys.platform == 'linux':
        print(f"Missing packages. Please install the following packages: (requests, edge_tts, ffmpeg-python, matplotlib) and FFmpeg. (not a package)")
        exit(1)
    wizardInput = input("Some required files are missing. Would you like to run the setup wizard? (y/n): ").strip().lower()
    if wizardInput == 'y':
        setup.install()
    else:
        print("Exiting the program. Please run the setup wizard or install the required packages manually. (Packages: requests, edge_tts, ffmpeg-python, matplotlib) and FFmpeg.")
        exit(1)

if os.system('ffmpeg') != 0:
    run('Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser')
    run("winget install Gyan.FFmpeg")

# Fetch the word of the day from the API
apiGet = requests.get('https://random-word-api.herokuapp.com/word')

customWord = False

word = "CustomWord"

voice = 'en-US-JennyNeural'

if not customWord:
    word = ""
    for i, letter in enumerate(json.loads(apiGet.content)[0]):
        if i==0:
            word += letter.upper()
        else:
            word += letter

mp3_input = 'input.mp3'
video_output = 'output.mp4'
width = 1920
height = 1080

# Play the word of the day using edge_tts

async def main():
    wordOfTheDay = 'The word of the day, is. ' + word
    print(f"Word: {word}")

    communicate = edge_tts.Communicate(wordOfTheDay, voice=voice)
    await communicate.save(mp3_input)

asyncio.run(main())

# Note: The above code requires an internet connection to fetch the word of the day.

# Check if the mp3 file is created in the current directory.
if os.path.exists(mp3_input):
    print(f'The audio file has been created successfully as {mp3_input}.')
else:
    print("Failed to create the audio file.")

# Make a video out of the audio file using ffmpeg

def create_video_from_audio(mp3_input,video_output):

    # Make the base mp4 with a blue background, just for demonstration

    vid = ffmpeg.input(f'color=c=white:s={width}x{height}:r=30:d=10', f='lavfi')

    vid = ffmpeg.drawtext(vid, text='The word of the day is..', fontfile='ARIAL.TTF', fontsize=100, fontcolor='black', x=f'({width}/2)-(text_w/2)', y=f'{height}/2', escape_text=True, enable="lt(n,60)", timecode_rate=30)

    vid = ffmpeg.drawtext(vid, text='2025 - Selavyn', fontfile='ARIAL.TTF', fontsize=50, fontcolor='gray', x=f'({width}/2)-(text_w/2)', y=f'{height}/1.1', escape_text=True, timecode_rate=30)

    vid = ffmpeg.drawtext(vid, text=word, fontfile='ARIAL.TTF', fontsize=100, fontcolor='black', x=f'({width}/2)-(text_w/2)', y=f'{height}/2', escape_text=True, enable="gt(n,75)*lt(n,110)", timecode_rate=30)

    mus = ffmpeg.input(mp3_input)
    
    out = ffmpeg.output(vid, mus, video_output, vcodec='libx264', acodec='mp3', shortest=None).run(overwrite_output=True)

    print(f'Video created as {video_output}')

create_video_from_audio(mp3_input, video_output)

os.system(f'start {video_output}')