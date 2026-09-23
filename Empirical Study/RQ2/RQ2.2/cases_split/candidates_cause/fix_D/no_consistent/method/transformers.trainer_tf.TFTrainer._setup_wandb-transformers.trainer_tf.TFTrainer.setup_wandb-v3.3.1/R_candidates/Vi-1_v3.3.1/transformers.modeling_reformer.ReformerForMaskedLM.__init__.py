    def __init__(self, config):
        super().__init__(config)
        assert (
            not config.is_decoder
        ), "If you want to use `ReformerForMaskedLM` make sure `config.is_decoder=False` for bi-directional self-attention."
        self.reformer = ReformerModel(config)
        self.lm_head = ReformerOnlyLMHead(config)

        self.init_weights()
