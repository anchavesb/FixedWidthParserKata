import argparse
import os.path
from parser import *


def is_valid_file(arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


if __name__ == "__main__":
    # Parse cmd line
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec_json", help="JSON Spec", type=argparse.FileType('r'), required=True)
    parser.add_argument("--input_file", help="Fixed width file", type=is_valid_file, required=True)
    parser.add_argument("--output_file", help="Fixed width file", required=True)
    parser.add_argument("--output_delimiter", help="Delimiter", default=',')

    args = parser.parse_args()

    if args:
        spec_dict = json.load(args.spec_json)
        spec = FixedWidthSpec(spec_dict)
        parser = FixedWidthParser(spec, args.output_delimiter)
        parser.parse(args.input_file, args.output_file)