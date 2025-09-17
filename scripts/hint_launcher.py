#!/bin/python

import os, sys

"""
Launch hints and run the script given on the command line with the hint-url.
Allows the count argument to be given as --count
"""

qcommand = ""
if "QUTE_COUNT" in os.environ:
    qcommand = f"{qcommand} --count {os.environ['QUTE_COUNT']}"
if "QUTE_URL" in os.environ:
    qcommand = f"{qcommand} --qute-url {os.environ['QUTE_URL']}"
if "QUTE_TITLE" in os.environ:
    qcommand = f"{qcommand} --qute-title \"{os.environ['QUTE_TITLE']}\""
if "QUTE_SELECTED_TEXT" in os.environ and os.environ["QUTE_SELECTED_TEXT"]:
    qcommand = f"{qcommand} --qute-selected-text '{os.environ['QUTE_SELECTED_TEXT'].replace("\n", " ").strip()}'"
if "QUTE_TAB_INDEX" in os.environ:
    qcommand = f"{qcommand} --qute-tab-index {os.environ['QUTE_TAB_INDEX']}"

if "--rapid" in sys.argv:
    qcommand = f"hint --rapid all spawn --userscript {sys.argv[1]} {{hint-url}} {qcommand}"
else:
    qcommand = f"hint all spawn --userscript {sys.argv[1]} {{hint-url}} {qcommand}"
# qcommand = f""":hint links spawn --userscript "{qcommand}" """
with open(os.environ['QUTE_FIFO'], "w") as f:
    f.write(qcommand)
