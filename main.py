import requests
import json
import asyncio
import edge_tts
import os
import ffmpeg


# Fetch the word of the day from the API
apiGet = requests.get('https://random-word-api.herokuapp.com/word')

mp3_input = 'input.mp3'
video_output = 'output.mp4'
# Play the word of the day using edge_tts
# Ensure you have the edge_tts library installed: pip install edge-tts
async def main():
    wordOfTheDay = 'The word of the day, is. ' + json.loads(apiGet.content)[0]
    print(f"Word: {wordOfTheDay}")

    communicate = edge_tts.Communicate(wordOfTheDay, voice='en-US-JennyNeural')
    await communicate.save(mp3_input)

asyncio.run(main())

# Note: The above code requires an internet connection to fetch the word of the day.

# Check if the output.mp3 file is created in the current directory.
if os.path.exists('output.mp3'):
    print(f'The audio file has been created successfully as {mp3_input}.')
else:
    print("Failed to create the audio file.")

# Make a video out of the audio file using moviepy

def create_video_from_audio(mp3_input,video_output):

    # Make the base mp4 with a blue background, just for demonstration

    vid = ffmpeg.input('color=c=blue:s=1280x720:r=30:d=10', f='lavfi')

    mus = ffmpeg.input(mp3_input)
    
    out = ffmpeg.output(vid, mus, video_output, vcodec='libx264', acodec='aac', shortest=None).run(overwrite_output=True)

    print(f'Video created as {video_output}')

create_video_from_audio(mp3_input, video_output)