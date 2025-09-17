#!/bin/python3

"""
arguments
    1: url (str)
    2: modifier (int | default 1) What should be added to the numbers in the url
    3: which (comma separated numbers | default []): Which numbers in the url should be modified
    4: new_tab (default False): Whether to open in new tab.

    6: loop option. E.g., 1998-99 -> 1999-00 (currently it goes to 1999-100)
e.g.
    python this.py http://lib.com/124/post/
    # Add -1 to all numbers in link and open in new tab
    python this.py http://lib.com/124/post/1 -1 "" True

"""
import sys, re, os
from urllib.parse import unquote

def increment_numbers_at_indices(s, indices, modifier):
    def increment_match(match):
        new_num = f"{(int(match.group(0)) + modifier):>0{len(match.group(0))}}"
        # Ensure loop around if negative number. E.g., 00+(-1) -> -1 -> 99
        if int(new_num) < 0:
            new_num = f"{10**len(match.group(0))+int(new_num):>0{len(match.group(0))}}"
        return new_num
        # return str(int(match.group(0)) + modifier)
    
    pattern = r'\d+'
    matches = re.findall(pattern, s)
    num_matches = len(matches)
    for i in range(len(indices)):
        if indices[i] < 0: indices[i] = (num_matches+indices[i])

    result = list(s)
    offset = 0
    matches = re.finditer(pattern, s)
    
    for i, match in enumerate(matches):
        if i in indices or not indices:
            start, end = match.span()
            result[start + offset:end + offset] = increment_match(match)
            offset += len(increment_match(match)) - (end - start)
    
    return ''.join(result)



if __name__ == "__main__":
    assert(len(sys.argv) > 1)
    string = unquote(sys.argv[1])
    modifier = 1 if len(sys.argv) <= 2 else int(sys.argv[2])
    if len(sys.argv) > 3:
        which = [] if sys.argv[3] == "" else [int(x) for x in sys.argv[3].split(",")]
    else: which = []
    tab = False if len(sys.argv) < 5 else bool(sys.argv[4])
    if "QUTE_COUNT" in os.environ:
        modifier *= int(os.environ["QUTE_COUNT"])


    result = increment_numbers_at_indices(string, which, modifier)

    cmd = f"open -t {result}" if tab else f"open {result}"

    print(cmd) 
    with open(os.environ["QUTE_FIFO"], "a") as f:
        f.write(cmd)
