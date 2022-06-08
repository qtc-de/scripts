#!/bin/bash

if [[ $# -ne 1 ]]; then 
    echo "$0 <dir>"
    exit 1

elif [[ ! -d $1 ]]; then
    echo "[-] Error: '$1' is not a directory."
    exit 1
fi

FILENAME="$1"
ARCHIVE="/tmp/send_$(date +%s%N).tar"

HOST="<HOST>"
PORT="<PORT>"

tar -cvf "${ARCHIVE}" "${FILENAME}" &>/dev/null

if [[ $? -ne 0 ]]; then
    echo "[-] Unable to create tar archive."
    echo "[-] Aborting."

else
    echo "[+] Send file '${ARCHIVE}' to '${HOST}:${PORT}'"
    echo "[+] Checksum: $(md5sum "${ARCHIVE}" | cut -d' ' -f1)"

    nc --send-only ${HOST} ${PORT} < "${ARCHIVE}"

    if [[ $? -ne 0 ]]; then
        echo "[-] ncat transfer failed."
    fi
fi

if [[ -f "${ARCHIVE}" ]]; then
    rm "${ARCHIVE}"
fi
