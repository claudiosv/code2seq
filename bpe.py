import os
import sys
import dataprep.bpepkg.bpe_encode as bpe_encode
from dataprep.bpepkg.merge import MergeList, read_merges
from pathlib import Path


def filterJunk(token):
    junk = ["`w", "w`", "[", "]", "{", "}", "|"]

    if token in junk:
        return False
    else:
        return True


def main():
    filepath = sys.argv[2]
    merges = read_merges(
        "/Users/claudio/Projects/dataprep/dataprep/data/bpe/case/1k/merges.txt"
    )

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()
    cnt = 0
    with open(filepath) as fp, open(filepath + ".bpe.txt", "w") as writer:
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
                    # filtered_bpe_2 = list(filter(filterJunk, bpe_2))
                    path[0] = "|".join(bpe_2)
                    
                if (
                    path[len(path) - 1] != "METHOD_NAME"
                    and path[len(path) - 1] != "<NUM>"
                    and len(path[len(path) - 1]) > 2
                ):
                    bpe_3 = bpe_encode.encode_word(path[len(path) - 1].rstrip(), merges)
                    # filtered_bpe_3 = list(filter(filterJunk, bpe_3))
                    path[len(path) - 1] = "|".join(bpe_3)
                contexts.append(",".join(path))

            writer.write(split_line[0] + " " + " ".join(contexts) + "\n")

            cnt += 1
    print("Num of lines {}".format(cnt))


if __name__ == "__main__":
    main()

