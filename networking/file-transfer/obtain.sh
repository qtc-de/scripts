#!/bin/bash

if [[ $# -ne 1 ]]; then 
    echo "$0 <filename>"
    exit 1
fi

FILENAME="$1"
PORT="<PORT>"

echo "[+] Waiting for incomming connection..."
nc --recv-only -vnlp ${PORT} 1> "${FILENAME}" 2> /dev/null

if [[ $? -ne 0 ]]; then
    echo "[-] ncat transfer failed."
    echo "[-] Aborting."
    rm -f "${FILENAME}"

else
    echo "[+] Saved file to '${FILENAME}'"
    echo "[+] Checksum: $(md5sum "${FILENAME}" | cut -d' ' -f1)"
fi
