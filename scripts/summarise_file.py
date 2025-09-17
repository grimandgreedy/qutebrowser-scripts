#!/bin/python

import sys, os
import tempfile
import subprocess
from ollama import chat
from ollama import ChatResponse
import argparse
import html
import random
import string

"""
Generate a summary of a file using a local ollama model.

Examples:

python ~/scripts/summarise_file.py /tmp/tmpvw32y2el.txt --model mistral --word-count "600-800"
"""

def summarize_file(filename, model="mistral:latest", word_count="400-600"):
    try:
        # Open the file and read its content
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
            
        # Use given model to generate a summary
        response: ChatResponse = chat(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': f"{text}\n\nPlease write a concise summary of the above article in {word_count} words.",
                },
            ],
        )

        # print(response['message']['content'])
        print(response)

        return response['message']['content']
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        return None

def display_message(msg="", launched_from_qutebrowser=False):
    if launched_from_qutebrowser:
        try:
            with open(os.environ["QUTE_FIFO"], "w") as f:
                f.write(f"message-info '{msg}'\n")
        except:
            pass
    else:
        print(msg)

def convert_text_to_html(text, title=""):

    # Escape HTML special characters
    escaped_text = html.escape(text)

    # HTML structure with bigger text
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    """
    if title:
        html_content += f"""\n<title>{html.escape(title)}</title>\n"""
    html_content += f"""
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 24px;
            padding: 1em;
            background-color: #f4f4f4;
        }}
        .content {{
            background-color: #fff;
            padding: 1em;
            border-radius: 6px;
            box-shadow: 0 0 12px rgba(0,0,0,0.1);
            line-height: 1.6;
        }}
    </style>
</head>
<body>"""
    if title:
        html_content += f"""\n<h1> {title} </h1>\n"""
    html_content += f"""
    <div class="content">
        {escaped_text}
    </div>
</body>
</html>
"""

    # Generate random filename and save to /tmp
    random_string = ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(24))
    random_filename = f"{random_string}.html"
    output_path = os.path.join('/tmp', random_filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_path

def main():
    parser = argparse.ArgumentParser(description='Summarize a text file using Ollama')
    parser.add_argument('filename', help='The name of the input file')
    parser.add_argument('--model', default="mistral:latest", help='Ollama model to use for summarization')
    parser.add_argument('--popup', action="store_true", help='Flag to indicate if there should be an nvim popup window displayed with the output.')
    parser.add_argument('--word-count', default="400 to 600", help='How many words should the summary be?')
    parser.add_argument('-o', '--output-file', type=str, default="", help='Output the summary to a specified file')
    parser.add_argument('--qb-html', action="store_true", default=None, help='Create a summary, create a html file, and open it with qutebrowser.')

    args = parser.parse_args()
    filename = os.environ["QUTE_TEXT"] if "QUTE_TEXT" in os.environ else args.filename
    launched_from_qutebrowser = True if "QUTE_TEXT" in os.environ else False
    
    display_message(f"Creating summary using '{args.model}'", launched_from_qutebrowser)

    # Generate
    summary = summarize_file(filename, model=args.model, word_count=args.word_count)

    # Display summary
    if summary is not None:
        display_message("Summary created.", launched_from_qutebrowser)

        if args.qb_html:
            title = os.environ["QUTE_TITLE"] if "QUTE_TITLE" in os.environ else ""
            fname = convert_text_to_html(summary, title)
            with open(os.environ["QUTE_FIFO"], "w") as f:
                f.write(f"open -t {fname}")
            sys.exit(0)

        elif args.output_file:
            os.makedirs(os.path.dirname(args.output_file.strip()), exist_ok=True)
            with open(args.output_file.strip(), "w") as f:
                f.write(summary)

        elif args.popup:
            with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmpfile:
                tmpfile.write(summary)
                tmpfile_path = tmpfile.name
            cmd = f"kitty -e --class=reader-class nvim -i NONE -c 'setlocal bt=nofile' -c 'setlocal signcolumn=no' -c 'normal ,cj' -c 'colorscheme default' -c 'nohl' -c '0' {tmpfile_path}"
            subprocess.run(cmd, shell=True)

        else:
            print(summary)
    else:
        display_message(f"Failed to create summary.", launched_from_qutebrowser)
        sys.exit(1)

if __name__ == "__main__":
    main()
