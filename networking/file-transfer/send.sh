#!/bin/bash

if [[ $# -ne 1 ]]; then 
    echo "$0 <filename>"
    exit 1

elif [[ ! -f $1 ]]; then
    echo "[-] Error: '$1' is not a file."
    exit 1
fi

PORT="<PORT>"
HOST="<HOST>"
FILENAME="$1"

nc --send-only ${HOST} ${PORT} < "${FILENAME}" 2>/dev/null

if [[ $? -ne 0 ]]; then
    echo "[-] ncat transfer failed."
    echo "[-] Aborting."
    exit 1
fi

echo "[+] Send file '${FILENAME}' to '${HOST}:${PORT}'"
echo "[+] Checksum: $(md5sum "${FILENAME}" | cut -d' ' -f1)"
