try:
    import requests
    import json
    import asyncio
    import edge_tts
    import os
    import ffmpeg
    import matplotlib.font_manager
    import subprocess
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please run 'pip install requests edge-tts ffmpeg-python matplotlib' to install the required packages.")
    exit(1)


# Fetch the word of the day from the API
apiGet = requests.get('https://random-word-api.herokuapp.com/word')

word = ""

for i, letter in enumerate(json.loads(apiGet.content)[0]):
    if i==0:
        word += letter.upper()
    else:
        word += letter

mp3_input = 'input.mp3'
video_output = 'output.mp4'
width = 1280
height = 720

# Play the word of the day using edge_tts

async def main():
    wordOfTheDay = 'The word of the day, is. ' + json.loads(apiGet.content)[0]
    print(f"Word: {word}")

    communicate = edge_tts.Communicate(wordOfTheDay, voice='en-US-JennyNeural')
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

    vid = ffmpeg.drawtext(vid, text='The word of the day is..', fontfile='ARIAL.TTF', fontsize=64, fontcolor='black', x=f'({width}/2)-(text_w/2)', y=f'{height}/2', escape_text=True, enable="lt(n,60)", timecode_rate=30)

    vid = ffmpeg.drawtext(vid, text=word, fontfile='ARIAL.TTF', fontsize=64, fontcolor='black', x=f'({width}/2)-(text_w/2)', y=f'{height}/2', escape_text=True, enable="gt(n,75)*lt(n,110)", timecode_rate=30)

    mus = ffmpeg.input(mp3_input)
    
    out = ffmpeg.output(vid, mus, video_output, vcodec='libx264', acodec='mp3', shortest=None).run(overwrite_output=True)

    print(f'Video created as {video_output}')

create_video_from_audio(mp3_input, video_output)

os.system(f'ffplay -autoexit {video_output}')