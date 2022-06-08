#!/bin/bash

PORT="<PORT>"
HOST="<HOST>"
ARCHIVE="/tmp/obtain_$(date +%s%N).tar"

nc --recv-only ${HOST} ${PORT} > "${ARCHIVE}" 2>/dev/null

if [[ $? -ne 0 ]]; then
    echo "[-] ncat transfer failed."
    echo "[-] Aborting."

else
    echo "[+] Saved file to '${ARCHIVE}'"
    echo "[+] Checksum: $(md5sum "${ARCHIVE}" | cut -d' ' -f1)"

    tar -xvf "${ARCHIVE}" &> /dev/null
fi

if [[ -f "${ARCHIVE}" ]]; then
    rm "${ARCHIVE}"
fi
