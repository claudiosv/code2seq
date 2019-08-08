import os
import sys
from pathlib import Path
from argparse import ArgumentParser
import statistics


def main():

    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        dest="input_filename",
        help="File to read from",
        metavar="INPUT_FILE",
    )

    args = parser.parse_args()

    input_filename = args.input_filename


    if not os.path.isfile(input_filename):
        print("File path {} does not exist. Exiting...".format(input_filename))
        sys.exit()

    cnt = 0
    counts = []
    with open(input_filename) as fp:
        for line in fp:
            line = line.rstrip()
            split_line = line.split(" ")
            split_target = split_line[0].split("|")
            counts.append(len(split_target))
            cnt += 1
    print("Num of lines {}".format(cnt))
    print("Max Part length: ", max(counts))
    print("Avg part length: ", sum(counts)/len(counts))
    print("Min part length: ", min(counts))
    print("Median part length: ", statistics.median(counts))


if __name__ == "__main__":
    main()

