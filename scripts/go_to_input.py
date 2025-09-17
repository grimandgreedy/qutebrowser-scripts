#!/bin/python

import os, time

count = int(os.environ["QUTE_COUNT"])-1 if "QUTE_COUNT" in os.environ else 0

if "QUTE_FIFO" in os.environ:
    with open(os.environ["QUTE_FIFO"], "w") as f:
        f.write("hint --mode number inputs")
        f.flush()
        time.sleep(1/100)
        f.write(f"fake-key -g {count}")
