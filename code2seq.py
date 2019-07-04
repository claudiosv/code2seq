from argparse import ArgumentParser
from comet_ml import Experiment
import comet_ml

from config import Config
from interactive_predict import InteractivePredictor
from model import Model
import os

if __name__ == "__main__":
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
    parser = ArgumentParser()
    parser.add_argument(
        "-d",
        "--data",
        dest="data_path",
        help="path to preprocessed dataset",
        required=False,
    )
    parser.add_argument(
        "-te",
        "--test",
        dest="test_path",
        help="path to test file",
        metavar="FILE",
        required=False,
    )

    parser.add_argument(
        "-s",
        "--save_prefix",
        dest="save_path_prefix",
        help="path to save file",
        metavar="FILE",
        required=False,
    )
    parser.add_argument(
        "-l",
        "--load",
        dest="load_path",
        help="path to saved file",
        metavar="FILE",
        required=False,
    )
    parser.add_argument(
        "--release",
        action="store_true",
        help="if specified and loading a trained model, release the loaded model for a smaller model "
        "size.",
    )
    parser.add_argument("--predict", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    if args.debug:
        config = Config.get_debug_config(args)
    else:
        config = Config.get_default_config(args)

    model = Model(config)
    print("Created model")
    if config.TRAIN_PATH:
        model.train()
    if config.TEST_PATH and not args.data_path:
        results, precision, recall, f1 = model.evaluate()
        print("Accuracy: " + str(results))
        print(
            "Precision: "
            + str(precision)
            + ", recall: "
            + str(recall)
            + ", F1: "
            + str(f1)
        )
    if args.predict:
        predictor = InteractivePredictor(config, model)
        predictor.predict()
    # if args.optimize:
    #     optimizer = comet_ml.Optimizer()
    #     params = """
    #     optimizer categorical {sgd,adam,RMSprop} [adam]
    #     attention categorical {scaled_luong,luong,normalized_bahdanau,bahdanau}[luong]
    #     EMBEDDINGS_DROPOUT_KEEP_PROB real [0,1] [0.75]
    #     RNN_DROPOUT_KEEP_PROB real [0,1] [0.5]
    #     BATCH_SIZE ordinal {16,32,64,128} [64]
    #     RNN_SIZE ordinal {128,256,512} [256]
    #     EMBEDDINGS_SIZE ordinal {64,128,256} [128]
    #     DECODER_SIZE ordinal {160,320,400}
    #     BIRNN categorical {true,false} [true]
    #     architecture categorical {gru,lstm} [lstm]
    #     """
    #     optimizer.set_params(params)

    #     i = 0
    #     while True:
    #         # 4. Get a suggestion
    #         try:
    #             suggestion = optimizer.get_suggestion()
    #         except comet_ml.NoMoreSuggestionsAvailable:
    #             # get_suggestion() will raise when no new suggestions
    #             # are available
    #             break
    #         suggestion[key]
    #         # Build model, train, and get score:
    #         print("Trial:", i)

    #         # 5. Report the score back, maximizes:
    #         suggestion.report_score("accuracy", score)
    #         i += 1
    if args.release and args.load_path:
        print("Started in release mode")
        model.evaluate(release=True)
    model.close_session()
