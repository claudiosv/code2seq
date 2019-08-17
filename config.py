import json

class Config:
    @staticmethod
    def get_default_config(args):
        config = Config(args)
        config.NUM_EPOCHS = 3000  # 3000
        config.SAVE_EVERY_EPOCHS = 1
        config.PATIENCE = 5
        config.BATCH_SIZE = 256  # 512
        config.TEST_BATCH_SIZE = 256  # 256
        config.READER_NUM_PARALLEL_BATCHES = 1
        config.SHUFFLE_BUFFER_SIZE = 10000
        config.CSV_BUFFER_SIZE = 100 * 1024 * 1024  # 100 MB
        config.MAX_CONTEXTS = 200
        # 200  # the number of sampled paths from each example (which we set to 200 in the final models).
        config.SUBTOKENS_VOCAB_MAX_SIZE = 7300  # 190000
        config.TARGET_VOCAB_MAX_SIZE = 8700  # 27000
        config.EMBEDDINGS_SIZE = 128  # 128  # dtokens = dnodes = dhidden = dtarget = 128
        config.RNN_SIZE = 256  # 128 * 2  # Two LSTMs to embed paths, each of size 128
        config.DECODER_SIZE = 320  # 320
        config.NUM_DECODER_LAYERS = 1
        config.MAX_PATH_LENGTH = 8 + 1
        config.MAX_NAME_PARTS = 5
        config.MAX_TARGET_PARTS = 6
        config.EMBEDDINGS_DROPOUT_KEEP_PROB = 0.75  # dropout 0.25
        config.RNN_DROPOUT_KEEP_PROB = 0.5
        # recurrent dropout of 0.5 on the LSTM that encodes the AST paths.
        config.BIRNN = True
        config.GRU = False
        config.RANDOM_CONTEXTS = True
        config.BEAM_WIDTH = 0
        config.USE_MOMENTUM = True
        config.NORM_OR_SCALE = False
        config.ATTENTION = "luong"  # "bahdanau"
        config.SPARSE_CROSS_ENT = True
        config.PENALIZE_UNK = False
        return config

    @staticmethod
    def get_config_json(args, jsonConfig):
        otherConfig = json.load(jsonConfig)
        config = Config(args)
        config.NUM_EPOCHS = otherConfig["NUM_EPOCHS"]  # 3000
        config.SAVE_EVERY_EPOCHS = otherConfig["SAVE_EVERY_EPOCHS"] 
        config.PATIENCE = otherConfig["PATIENCE"] 
        config.BATCH_SIZE = otherConfig["BATCH_SIZE"] 
        config.TEST_BATCH_SIZE = otherConfig["TEST_BATCH_SIZE"] 
        config.READER_NUM_PARALLEL_BATCHES = otherConfig["READER_NUM_PARALLEL_BATCHES"] 
        config.SHUFFLE_BUFFER_SIZE = otherConfig["SHUFFLE_BUFFER_SIZE"] 
        config.CSV_BUFFER_SIZE = otherConfig["CSV_BUFFER_SIZE"] 
        config.MAX_CONTEXTS = otherConfig["MAX_CONTEXTS"] 
        # 200  # the number of sampled paths from each example (which we set to 200 in the final models).
        config.SUBTOKENS_VOCAB_MAX_SIZE = otherConfig["SUBTOKENS_VOCAB_MAX_SIZE"] 
        config.TARGET_VOCAB_MAX_SIZE = otherConfig["TARGET_VOCAB_MAX_SIZE"] 
        config.EMBEDDINGS_SIZE = otherConfig["EMBEDDINGS_SIZE"] 
        config.RNN_SIZE = otherConfig["RNN_SIZE"] 
        config.DECODER_SIZE = otherConfig["DECODER_SIZE"] 
        config.NUM_DECODER_LAYERS = otherConfig["NUM_DECODER_LAYERS"] 
        config.MAX_PATH_LENGTH = otherConfig["MAX_PATH_LENGTH"] 
        config.MAX_NAME_PARTS = otherConfig["MAX_NAME_PARTS"] 
        config.MAX_TARGET_PARTS = otherConfig["MAX_TARGET_PARTS"] 
        config.EMBEDDINGS_DROPOUT_KEEP_PROB = otherConfig["EMBEDDINGS_DROPOUT_KEEP_PROB"] 
        config.RNN_DROPOUT_KEEP_PROB = otherConfig["RNN_DROPOUT_KEEP_PROB"] 
        # recurrent dropout of 0.5 on the LSTM that encodes the AST paths.
        config.BIRNN = otherConfig["BIRNN"] 
        config.GRU = otherConfig["GRU"] 
        config.RANDOM_CONTEXTS = otherConfig["RANDOM_CONTEXTS"] 
        config.BEAM_WIDTH = otherConfig["BEAM_WIDTH"] 
        config.USE_MOMENTUM = otherConfig["USE_MOMENTUM"] 
        config.NORM_OR_SCALE = otherConfig["NORM_OR_SCALE"] 
        config.ATTENTION = otherConfig["ATTENTION"] 
        config.SPARSE_CROSS_ENT = otherConfig["SPARSE_CROSS_ENT"] 
        config.PENALIZE_UNK = otherConfig["PENALIZE_UNK"] 
        return config

    def take_model_hyperparams_from(self, otherConfig):
        self.EMBEDDINGS_SIZE = otherConfig.EMBEDDINGS_SIZE
        self.RNN_SIZE = otherConfig.RNN_SIZE
        self.DECODER_SIZE = otherConfig.DECODER_SIZE
        self.NUM_DECODER_LAYERS = otherConfig.NUM_DECODER_LAYERS
        self.BIRNN = otherConfig.BIRNN
        self.GRU = otherConfig.GRU

        if self.DATA_NUM_CONTEXTS <= 0:
            self.DATA_NUM_CONTEXTS = otherConfig.DATA_NUM_CONTEXTS

    def __init__(self, args):
        self.NUM_EPOCHS = 0
        self.SAVE_EVERY_EPOCHS = 0
        self.PATIENCE = 0
        self.BATCH_SIZE = 0
        self.TEST_BATCH_SIZE = 0
        self.READER_NUM_PARALLEL_BATCHES = 0
        self.SHUFFLE_BUFFER_SIZE = 0
        self.CSV_BUFFER_SIZE = None
        self.TRAIN_PATH = args.data_path
        self.TEST_PATH = args.test_path if args.test_path is not None else ""
        self.DATA_NUM_CONTEXTS = 0
        self.MAX_CONTEXTS = 0
        self.SUBTOKENS_VOCAB_MAX_SIZE = 0
        self.TARGET_VOCAB_MAX_SIZE = 0
        self.EMBEDDINGS_SIZE = 0
        self.RNN_SIZE = 0
        self.DECODER_SIZE = 0
        self.NUM_DECODER_LAYERS = 0
        self.SAVE_PATH = args.save_path_prefix
        self.LOAD_PATH = args.load_path
        self.MAX_PATH_LENGTH = 0
        self.MAX_NAME_PARTS = 0
        self.MAX_TARGET_PARTS = 0
        self.EMBEDDINGS_DROPOUT_KEEP_PROB = 0
        self.RNN_DROPOUT_KEEP_PROB = 0
        self.BIRNN = False
        self.GRU = True
        self.RANDOM_CONTEXTS = True
        self.BEAM_WIDTH = 1
        self.USE_MOMENTUM = True
        self.RELEASE = args.release
        self.ATTENTION = "luong"
        self.PENALIZE_UNK = False

    @staticmethod
    def get_debug_config(args):
        config = Config(args)
        config.NUM_EPOCHS = 3000
        config.SAVE_EVERY_EPOCHS = 100
        config.PATIENCE = 200
        config.BATCH_SIZE = 7
        config.TEST_BATCH_SIZE = 7
        config.READER_NUM_PARALLEL_BATCHES = 1
        config.SHUFFLE_BUFFER_SIZE = 10
        config.CSV_BUFFER_SIZE = None
        config.MAX_CONTEXTS = 5
        config.SUBTOKENS_VOCAB_MAX_SIZE = 190000
        config.TARGET_VOCAB_MAX_SIZE = 27000
        config.EMBEDDINGS_SIZE = 19
        config.RNN_SIZE = 10
        config.DECODER_SIZE = 11
        config.NUM_DECODER_LAYERS = 1
        config.MAX_PATH_LENGTH = 8 + 1
        config.MAX_NAME_PARTS = 5
        config.MAX_TARGET_PARTS = 6
        config.EMBEDDINGS_DROPOUT_KEEP_PROB = 1
        config.RNN_DROPOUT_KEEP_PROB = 1
        config.BIRNN = True
        config.GRU = False
        config.RANDOM_CONTEXTS = True
        config.BEAM_WIDTH = 0
        config.USE_MOMENTUM = False
        config.PENALIZE_UNK = False
        return config