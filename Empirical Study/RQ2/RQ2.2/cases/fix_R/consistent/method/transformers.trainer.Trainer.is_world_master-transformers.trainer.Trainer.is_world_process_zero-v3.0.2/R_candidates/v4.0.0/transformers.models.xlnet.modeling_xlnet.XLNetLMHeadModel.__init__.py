    def __init__(self, config):
        super().__init__(config)
        self.attn_type = config.attn_type
        self.same_length = config.same_length

        self.transformer = XLNetModel(config)
        self.lm_loss = nn.Linear(config.d_model, config.vocab_size, bias=True)

        self.init_weights()
