    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.num_hidden_layers = config.num_hidden_layers
        self.initializer_range = config.initializer_range
        self.output_attentions = config.output_attentions
        self.output_hidden_states = config.output_hidden_states
        self.return_dict = config.use_return_dict
        self.encoder = TFRobertaEncoder(config, name="encoder")
        self.pooler = TFRobertaPooler(config, name="pooler")
        # The embeddings must be the last declaration in order to follow the weights order
        self.embeddings = TFRobertaEmbeddings(config, name="embeddings")
