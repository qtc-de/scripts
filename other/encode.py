#!/usr/bin/env python3

import sys
import argparse
import urllib.parse


def encode_url(data):
    '''
    Applies URL encoding to the input data for URL special characters.
    Input data can be specified as string or raw bytes.

    Parameters:
        data                (string/bytes)      Input data

    Returns:
        string              (string)            URL encoded output
    '''
    return urllib.parse.quote_plus(data)


def encode_url_full(data):
    '''
    Takes a string or raw bytes as input and applies URL encoding to
    each character. If input is string, it is treated as utf-8 and
    multibyte characters are encoded as seperate URL encoded characters.

    Parameters:
        data                (string/bytes)      Input data

    Returns:
        string              (string)            URL encoded output
    '''
    if not isinstance(data, bytes):
        data = data.encode('utf-8')

    hex_form = data.hex()
    return_value = ''

    for i in range(0, len(hex_form), 2):
        return_value += '%' + hex_form[i:i+2]

    return return_value


parser = argparse.ArgumentParser(description='''Simple command line encoder.''')
parser.add_argument('encoding', nargs='?', default='url', choices=['url'], help='encoding to apply')
parser.add_argument('-f', '--full', action='store_true', help='apply encoding to all characters')

args = parser.parse_args()
stuff = sys.stdin.buffer.read()

if stuff[-1] == 10:
    stuff = stuff[:-1]

if args.encoding == 'url':

    if args.full:
        print(encode_url_full(stuff))
    else:
        print(encode_url(stuff))
