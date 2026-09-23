    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.num_hidden_layers = config.num_hidden_layers
        self.output_attentions = config.output_attentions
        self.output_hidden_states = config.output_hidden_states
        self.return_dict = config.use_return_dict

        self.embeddings = TFMobileBertEmbeddings(config, name="embeddings")
        self.encoder = TFMobileBertEncoder(config, name="encoder")
        self.pooler = TFMobileBertPooler(config, name="pooler")
