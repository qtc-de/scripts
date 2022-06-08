#!/bin/bash

if [[ $# -ne 1 ]]; then 
    echo "$0 <filename>"
    exit 1

elif [[ ! -f $1 ]]; then
    echo "[-] Error: '$1' is not a file."
    exit 1
fi

FILENAME=$1
PORT="<PORT>"

echo "[+] Serving file '${FILENAME}'"
echo "[+] Checksum: $(md5sum "${FILENAME}" | cut -d' ' -f1)"

nc --send-only -nvlp ${PORT} < "${FILENAME}" &>/dev/null

if [[ $? -ne 0 ]]; then
    echo "[-] ncat transfer failed."
    echo "[-] Aborting."
fi
