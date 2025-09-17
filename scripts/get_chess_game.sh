#!/bin/bash

copy_to_clipboard() {
    if command -v wl-copy &> /dev/null; then
        echo -n "${CHESS_GAME}" | wl-copy
        echo "Copied using wl-copy (Wayland)"
    elif command -v xclip &> /dev/null; then
        echo -n "${CHESS_GAME}" | xclip -selection clipboard
        echo "Copied using xclip"
    elif command -v xsel &> /dev/null; then
        echo -n "${CHESS_GAME}" | xsel --clipboard --input
        echo "Copied using xsel"
    elif command -v pbcopy &> /dev/null; then
        echo -n "${CHESS_GAME}" | pbcopy
        echo "Copied using pbcopy (macOS)"
    else
        echo "message-error 'Error: No supported clipboard manager found (xclip, xsel, wl-copy, pbcopy).'" >> $QUTE_FIFO
        exit 1
    fi
}

CHESS_GAME=$(grep -E '^\s*[a-h][1-8]\+?$|^[QBNRPKqbnrpk][a-h1-8]?[x]?[a-h][1-8]\+?#?$|^[a-h][x][a-h][1-8]\+?#?$|[a-h][x]?[a-h]?[1-8]?=[QBNRPKqbnrpk]\+?#?$|^O-O(-O)?\+?#?$' "${QUTE_TEXT}")

copy_to_clipboard



echo "message-info 'Game copied to clipboard.'" >> $QUTE_FIFO
