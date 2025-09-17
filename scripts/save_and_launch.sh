#!/bin/bash

# $1 : program
# $2 : URL

fname="${RANDOM}${RANDOM}"

wget "${2}" -O "/tmp/${fname}"

"$1" "/tmp/${fname}"
