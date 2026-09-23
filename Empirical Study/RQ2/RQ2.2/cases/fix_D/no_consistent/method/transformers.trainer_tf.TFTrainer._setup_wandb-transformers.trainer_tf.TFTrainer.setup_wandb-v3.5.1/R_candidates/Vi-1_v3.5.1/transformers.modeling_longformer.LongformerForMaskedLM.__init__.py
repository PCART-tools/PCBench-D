    def __init__(self, config):
        super().__init__(config)

        self.longformer = LongformerModel(config, add_pooling_layer=False)
        self.lm_head = LongformerLMHead(config)

        self.init_weights()
