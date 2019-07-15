import os
import sys
import dataprep.api.text as pp


def main():
    filepath = sys.argv[2]

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    # bag_of_words = {}
    cnt = 0
    with open(filepath) as fp, open(filepath + ".bpe.txt", "w") as writer:
        for line in fp:
            # print("line {} contents {}".format(cnt, line))
            split_line = line.split(" ")
            # apply BPE to split_line[0]
            bpe_1 = pp.bpe(split_line[0], bpe_codes_id="1k")
            print(bpe_1)
            split_line[0] = "|".join(bpe_1)
            contexts = []
            for i in range(1, len(split_line)):
                # print(split_line[i])
                path = split_line[i].split(",")
                if path[0] != "METHOD_NAME" and path[0] != "<NUM>":
                    # apply BPE to path[0]
                    # print("Applying BPE to " + path[0])

                    # container|[{}]|does|not|exist|creating
                    # ['`w', 'contain', 'er', 'w`', '|', '[', '{', '}', ']', '|', '`w', 'do', 'es', 'w`', '|', 'not', '|', '`w', 'ex', 'ist', 'w`', '|', '`w', 'cre', 'at', 'ing', 'w`']

                    bpe_2 = pp.bpe(path[0], bpe_codes_id="1k")
                    if "[" in bpe_2 or "{" in bpe_2:
                        print(path[0])
                        print(bpe_2)
                    path[0] = "|".join(bpe_2)
                if path[len(path) - 1] != "<NUM>":
                    # apply BPE
                    # print("Applying BPE to " + path[len(path) - 1])
                    bpe_3 = pp.bpe(path[len(path) - 1], bpe_codes_id="1k")
                    print(bpe_3)
                    path[len(path) - 1] = "|".join(bpe_3)
                # print(",".join(path))

                # print("\n\n")
                contexts.append(",".join(path))

            writer.write(split_line[0] + " " + " ".join(contexts))

            # record_word_cnt(line.strip().split(" "), bag_of_words)
            cnt += 1
    # sorted_words = order_bag_of_words(bag_of_words, desc=True)
    print("Num of lines {}".format(cnt))


# def order_bag_of_words(bag_of_words, desc=False):
#     words = [(word, cnt) for word, cnt in bag_of_words.items()]
#     return sorted(words, key=lambda x: x[1], reverse=desc)


# def record_word_cnt(words, bag_of_words):
#     for word in words:
#         if word != "":
#             if word.lower() in bag_of_words:
#                 bag_of_words[word.lower()] += 1
#             else:
#                 bag_of_words[word.lower()] = 1


if __name__ == "__main__":
    main()

