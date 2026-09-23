    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.block_sizes = config.block_sizes
        self.output_attentions = config.output_attentions
        self.output_hidden_states = config.output_hidden_states
        self.return_dict = config.use_return_dict

        self.embeddings = TFFunnelEmbeddings(config, name="embeddings")
        self.encoder = TFFunnelEncoder(config, name="encoder")
        self.decoder = TFFunnelDecoder(config, name="decoder")
