    def __init__(self, config):
        super().__init__(config)
        self.config = config
        assert (
            self.config.num_hidden_layers > 0
        ), "`config.attn_layers` is empty. Select at least one attn layer form ['lsh', 'local']"

        self.embeddings = ReformerEmbeddings(config)
        self.encoder = ReformerEncoder(config)

        self.init_weights()
