#!/bin/bash

if [[ $# -ne 1 ]]; then 
    echo "$0 <filename>"
    exit 1
fi

PORT="<PORT>"
HOST="<HOST>"
FILENAME="$1"

nc --recv-only ${HOST} ${PORT} > "${FILENAME}" 2>/dev/null

if [[ $? -ne 0 ]]; then
    echo "[-] ncat transfer failed."
    echo "[-] Aborting."

    if [[ -f "${FILENAME}" ]]; then
        rm "${FILENAME}"
    fi

    exit 1
fi

echo "[+] Saved file to '${FILENAME}'"
echo "[+] Checksum: $(md5sum "${FILENAME}" | cut -d' ' -f1)"
