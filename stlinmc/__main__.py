import argparse
import os

import validators

from stlinmc import minecraft
from stlinmc import voxel


def file_choices(parser, choices, fname):
    ext = os.path.splitext(fname)[1]
    if ext == '' or ext.lower() not in choices:
        if len(choices) == 1:
            parser.error(f'{fname} doesn\'t end with {choices}')
        else:
            parser.error(f'{fname} doesn\'t end with one of {choices}')
    return fname


def valid_ip(parser, ipin):
    valid = False
    try:
        validators.ip_address.ipv4(ipin)
        valid = True
    except validators.ValidationFailure:
        valid = False
    try:
        validators.url(ipin)
        valid = True
    except validators.ValidationFailure:
        valid = False
    if valid:
        return ipin
    else:
        parser.error(f'\'{ipin}\' is not a valid IP address or URL')


def run_parser():
    parser = argparse.ArgumentParser(description='Import STL into Minecraft')
    parser.add_argument(
        'input',
        type=lambda s: file_choices(parser, ('.stl'), s),
        help='Input STL file')
    parser.add_argument(
        'server',
        type=lambda s: valid_ip(parser, s),
        help='Minecraft Server IP')
    parser.add_argument(
        '--port',
        type=int,
        help='Raspberry Juice Port')
    parser.set_defaults(port=4711)
    args = parser.parse_args()
    return args


def main():
    args = run_parser()
    print(f"Generating voxels from {args.input}")
    voxels = voxel.import_stl_as_voxels(args.input)
    print(f"Sending voxels to {args.server}:{args.port}")
    minecraft.build_voxels(voxels, args.server, args.port)
    print("Sent build commands to server, Done!")


if __name__ == '__main__':
    main()
