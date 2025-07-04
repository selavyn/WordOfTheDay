# WordOfTheDay

This is a python script that uses ffmpeg, edge_tts, and matplotlib to fetch a random word from an API, generate its pronunciation using text-to-speech, and create a visual representation of the word.
It also includes a setup wizard to install necessary packages and FFmpeg if they are not already installed.
You can change customize the script.

To change the word, you can set the `customWord` variable to `True` and assign a value to the `word` variable.
To change the voice you can set the `voice` variable to a different voice string supported by edge_tts.
To change the video size, you can modify the `width` and `height` variables.