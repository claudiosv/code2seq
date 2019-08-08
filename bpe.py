import os
import sys
import dataprep.bpepkg.bpe_encode as bpe_encode
from dataprep.bpepkg.merge import MergeList, read_merges
from pathlib import Path
from argparse import ArgumentParser


def filterJunk(token):
    junk = ["`w", "w`", "[", "]", "{", "}", "|"]

    if token in junk:
        return False
    else:
        return True


def main():

    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        dest="input_filename",
        help="File to read from",
        metavar="INPUT_FILE",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_filename",
        help="File to write to",
        metavar="OUTPUT_FILE",
    )
    parser.add_argument("-m", "--merges", dest="merges_file", help="Merges file")

    args = parser.parse_args()

    input_filename = args.input_filename
    output_filename = args.output_filename

    merges = read_merges(args.merges_file)

    if not os.path.isfile(input_filename):
        print("File path {} does not exist. Exiting...".format(input_filename))
        sys.exit()
    if not os.path.isfile(output_filename):
        print("File path {} does not exist. Exiting...".format(output_filename))
        sys.exit()

    cnt = 0
    with open(input_filename) as fp, open(output_filename, "w") as writer:
        for line in fp:
            line = line.rstrip()
            split_line = line.split(" ")
            bpe_1 = bpe_encode.encode_word(split_line[0], merges)

            split_line[0] = "|".join(bpe_1)
            contexts = []

            for i in range(1, len(split_line)):
                path = split_line[i].split(",")

                if path[0] != "METHOD_NAME" and path[0] != "<NUM>" and len(path[0]) > 2:
                    bpe_2 = bpe_encode.encode_word(path[0], merges)
                    path[0] = "|".join(bpe_2)

                if (
                    path[len(path) - 1] != "METHOD_NAME"
                    and path[len(path) - 1] != "<NUM>"
                    and len(path[len(path) - 1]) > 2
                ):
                    bpe_3 = bpe_encode.encode_word(path[len(path) - 1].rstrip(), merges)
                    path[len(path) - 1] = "|".join(bpe_3)
                contexts.append(",".join(path))

            writer.write(split_line[0] + " " + " ".join(contexts) + "\n")
            # writer.write(" ".join(split_line) + "\n")

            cnt += 1
    print("Num of lines {}".format(cnt))


if __name__ == "__main__":
    main()

