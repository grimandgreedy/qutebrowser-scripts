#!/bin/python
"""
File: read_web_page.py
Author: grim
Date: 05/10/2024
Github: https://github.com/grimandgreedy
Description: Converts the text of a webpage to a wav file using piper tts
"""

import os 

import codecs
import random, string

def extract_readable_text_to_file(tmpdir="/tmp/"):
    """Extract readable text from the current Qutebrowser page and save to a file.

    This was adapted from the qutebrowser `readability` script

    Returns:
        str: Path to the temporary text file.
    """
    # Read the page's raw HTML
    with codecs.open(os.environ['QUTE_HTML'], 'r', 'utf-8') as source:
        data = source.read()

    try:
        # Try using breadability
        from breadability.readable import Article as reader
        doc = reader(data, url=os.environ['QUTE_URL'])
        content = doc.readable_text
    except ImportError:
        # Fallback to readability-lxml + BeautifulSoup
        from readability import Document
        from bs4 import BeautifulSoup

        doc = Document(data)
        html_summary = doc.summary()
        soup = BeautifulSoup(html_summary, "html.parser")
        content = soup.get_text()

    tmpfile = ''.join(random.choices(string.ascii_letters, k=16)) + ".txt"
    tmpfile = os.path.join(tmpdir, tmpfile)

    os.makedirs(os.path.dirname(tmpfile), exist_ok=True)

    # Write the plain text to the file
    with open(tmpfile, 'w') as f:
        f.write(content.strip())

    return tmpfile

def display_message(msg):
    with open(os.environ["QUTE_FIFO"], "w") as f:
        f.write(f"message-info '{msg}'\n")

if __name__ == "__main__":

    dir = "/tmp"
    voice_model_path = "~/Clone/Neural-Amy-TTS/models/amy_v1/model.onnx"

    display_message("Starting TTS.")

    tmpfile = extract_readable_text_to_file()

    os.system(f'cat "{tmpfile}" | piper-tts -m {voice_model_path} -f "{tmpfile}.wav"')

    display_message("TTS Completed.")

    os.system(f"mpv --profile=audio '{tmpfile}.wav'")
