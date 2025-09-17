## Putting it all togther

The requirements for each script can be seen below; this is all of it put together.

### Keybinds
```
## Some keybinds
# Config keybinds
config.bind(',cs', 'config-source')
config.bind(',cw', 'config-write-py --force')
config.bind(',ec', 'spawn --detach kitty sh -c "yazi ~/.config/qutebrowser/config.py"')


# Translate page
config.bind(',gt', ':open -t translate.google.com/translate?sl=auto&tl=en-US&u={url}')

# Image search
config.bind(',his', 'hint images run :open -t https://tineye.com/search?url={hint-url}')
config.bind(',hiS', 'hint images run :open -t https://yandex.com/images/search?rpt=imageview&url={hint-url}')

# Open externally
config.bind(',,c', 'spawn --detach chromium "{url}"')
config.bind(',,C', 'spawn --detach chromium --incognito "{url}"')
config.bind(',,f', 'spawn --detach firefox "{url}"')
config.bind(',,F', 'spawn --detach firefox --private-window "{url}"')

# Qutebrowser examine
config.bind(',,k', 'spawn --userscript /bin/kitty')
config.bind(',,h', '''spawn --userscript /bin/kitty sh -c "nvim -c 'setlocal bt=nofile' -c '%!html-beautify' ${QUTE_HTML}"''')
config.bind(',,t', '''spawn --userscript /bin/kitty sh -c "nvim  -c 'setlocal bt=nofile' ${QUTE_TEXT}"''')

# Adjust hints
config.bind('-', 'clear-messages ;; config-cycle --print fonts.hints "bold 13pt default_family" "bold 11pt default_family" "bold 9pt default_family" "bold 7pt default_family" "bold 5pt default_family" ;; fake-key <Escape> ;; hint', mode='hint')
config.bind('+', 'clear-messages ;; config-cycle --print fonts.hints "bold 5pt default_family" "bold 7pt default_family" "bold 9pt default_family" "bold 11pt default_family" "bold 13pt default_family" ;; fake-key <Escape> ;; hint', mode='hint')
config.bind('=', 'clear-messages ;; set fonts.hints "bold 11pt default_family" ;; fake-key <Escape> ;; hint', mode='hint')

config.bind('<Tab>', 'clear-messages ;; config-cycle --print hints.mode word letter number ;; fake-key <Escape> ;; hint', mode='hint')
```

### Userscripts
```
## Userscripts
# MPV
config.bind(',m', 'spawn --userscript hint_launcher.py ~/.config/qutebrowser/userscripts/mpv.py')
config.bind(',M', 'spawn --userscript ~/.config/qutebrowser/userscripts/mpv.py {url}')
config.bind(';m', 'spawn --userscript hint_launcher.py ~/.config/qutebrowser/userscripts/mpv.py --rapid')

# Copy chess game
config.bind(',gg', 'spawn --userscript get_chess_game.sh')

# Open images with system viewer
config.bind(',hv', 'hint all spawn --userscript save_and_launch.sh vimiv {hint-url}')

# Summarise current page
config.bind(',ls', 'spawn --userscript summarise_file.py $QUTE_HTML --qb-html --model mistral')
config.bind(',lS', 'spawn --userscript summarise_file.py $QUTE_HTML --popup --model mistral')

# Read aloud
config.bind(',ra', 'spawn --userscript read_aloud.py')

# Increment all URL numbers
config.bind('<Alt+x>', 'spawn --userscript incdecnums.py {url} -1')
config.bind('<Alt+a>', 'spawn --userscript incdecnums.py {url} 1')
config.bind('<Alt+Shift+x>', 'spawn --userscript incdecnums.py {url} -1 "" True')
config.bind('<Alt+Shift+a>', 'spawn --userscript incdecnums.py {url} 1 "" True')

# Navigate by anchors
config.bind('g]', 'spawn --userscript anchors.py 1')
config.bind('g[', 'spawn --userscript anchors.py -1')

# Go to nth input field
config.bind(',gi', 'spawn --userscript go_to_input.py')
```

## Userscripts
### mpv

Open videos with mpv. Videos will open in the same mpv instance. New instances can be created by running with a count. Any links opened with the same count will be run in the same instance.

```
config.bind(',m', 'spawn --userscript hint_launcher.py ~/.config/qutebrowser/userscripts/mpv.py')
config.bind(',M', 'spawn --userscript ~/.config/qutebrowser/userscripts/mpv.py {url}')
config.bind(';m', 'spawn --userscript hint_launcher.py ~/.config/qutebrowser/userscripts/mpv.py --rapid')
```

### get_chess_game.sh

This script uses a regular expression to find chess moves in webpage and copies them to the clipboard so that you can enter the game into another application for analysis.

**Note**: On some sites you may need to change the move notation in the settings from symbols to letters.

```
config.bind(',gg', 'spawn --userscript get_chess_game.sh')
```



### Open image with system image viewer

Open images with vimiv

```
config.bind(',hv', 'hint all spawn --userscript save_and_launch.sh vimiv {hint-url}')
```

### Summarise page

This script summarises a webpage using ollama. The model can be specified as you wish.

```
config.bind(',ls', 'spawn --userscript summarise_file.py $QUTE_HTML --qb-html --model mistral')
config.bind(',lS', 'spawn --userscript summarise_file.py $QUTE_HTML --popup --model mistral')
```

### Read aloud

For this script to work you will need to:

 - install `piper-tts`
 - Get a voice model for `piper-tts`
  - If you clone [this repo](https://github.com/sweetbbak/Neural-Amy-TTS) to `~/Clone` it will work out of the box.
 - You will need to install `breadability` or `readability-lxml` and `beautifulsoup4` using pip
  - `pip install readability-lxml beautifulsoup4`
  - `pip install breadability`

```
config.bind(',ra', 'spawn --userscript read_aloud.py')
```

### Increment/decrement numbers in URL

This script allows you to modify numbers in a url in may ways. You can specify which numbers and by how much they should be (in/de)cremented.

The most basic use is to (in/de)crement all numbers in a url--not just the last number as the qutebrowser inc/dec function does. 
 - This is useful for links such as `https://en.wikipedia.org/wiki/2024-25_Premier_League`.

<Alt+x>/<Alt+a> open the url in the same page, <Alt+Shift+x>/<Alt+Shift+a> open the url in a new tab.

```
config.bind('<Alt+x>', 'spawn --userscript incdecnums.py {url} -1')
config.bind('<Alt+a>', 'spawn --userscript incdecnums.py {url} 1')
config.bind('<Alt+Shift+x>', 'spawn --userscript incdecnums.py {url} -1 "" True')
config.bind('<Alt+Shift+a>', 'spawn --userscript incdecnums.py {url} 1 "" True')
```

### Navigate page by anchors

Get the page anchors and go to the next/previous anchor.

```
config.bind('g]', 'spawn --userscript anchors.py 1')
config.bind('g[', 'spawn --userscript anchors.py -1')
```

### Go to nth input

If this is run with a count then you can go to the nth input field. Useful if you know you want to go to the third input field of a page.

```
config.bind(',gi', 'spawn --userscript go_to_input.py')
```


























