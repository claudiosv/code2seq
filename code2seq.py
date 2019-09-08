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
        "-c",
        "--config",
        dest="config_path",
        help="path to config file",
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
        if args.config_path:
            with open(args.config_path, 'r') as f:
                config = Config.get_config_json(args, f)
                print("Successfully loaded config from " + str(args.config_path))
        else:
            config = Config.get_default_config(args)

    model = Model(config)
    print("Created model")
    if config.TRAIN_PATH:
        model.train()
    if config.TEST_PATH and not args.data_path:
        
        results, precision_a, recall_a, f1_a, precision_b, recall_b, f1_b, precision_g, recall_g, f1_g = model.evaluate()
        print("Dataset: " + config.TEST_PATH)
        print("Config: " + args.config_path)
        print("Model: " + args.load_path)
        print("Accuracy: " + str(results))
        print(
            "Alpha Precision: "
            + str(precision_a)
            + ", recall: "
            + str(recall_a)
            + ", F1: "
            + str(f1_a)
        )
        print(
            "Beta Precision: "
            + str(precision_b)
            + ", recall: "
            + str(recall_b)
            + ", F1: "
            + str(f1_b)
        )
        print(
            "Gamma Precision: "
            + str(precision_g)
            + ", recall: "
            + str(recall_g)
            + ", F1: "
            + str(f1_g)
        )
    if args.predict:
        predictor = InteractivePredictor(config, model)
        predictor.predict()
    if args.release and args.load_path:
        print("Started in release mode")
        model.evaluate(release=True)
    model.close_session()
