#!/usr/bin/env python3

import re
import argparse
import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# This script is basically a wrapper around the following GitHub repo: https://github.com/billchaison/VNCDecrypt
# As the repo suggests, the following script is just a python implementation of:
# echo -n <ENC> | xxd -r -p | openssl enc -des-cbc --nopad --nosalt -K e84ad660c4721ae0 -iv 0000000000000000 -d

parser = argparse.ArgumentParser(description='''Script to decrypt encrypted VNC passwords''')
parser.add_argument('ciphertext', help='encrypted VNC password')
args = parser.parse_args()

password_regex = re.compile("([a-fA-F0-9]{2},?){7}[a-fA-F0-9]{2}$")
encrypted_password = password_regex.search(args.ciphertext)

if not encrypted_password:
    print("[-] Unable to parse supplied password.")
    print("[-] Valid format: 01,02,03,04,05,06,07,08")
    print("[-] Valid format: hex:01,02,03,04,05,06,07,08")
    print("[-] Valid format: \"Password\"=hex:01,02,03,04,05,06,07,08")
    sys.exit(1)

encrypted_password = encrypted_password.string.replace(',', '')

if len(encrypted_password) != 16:
    print("[-] Supplied password does not match expected length of 8 bytes.")
    print("[-] Stopping decryption.")

else:
    ciphertext = binascii.unhexlify(encrypted_password)
    cipher = Cipher(algorithms.TripleDES(binascii.unhexlify("e84ad660c4721ae0")), mode=modes.CBC(b'\x00' * 8))
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()

    try:
        print("[+] Decrypted password: " + decrypted.decode('utf-8'))

    except UnicodeDecodeError:
        print("[-] Password contains invalid Unicode sequences. Decryption result is probably junk.")
        print(b'[-] Decrypted: ' + decrypted)
