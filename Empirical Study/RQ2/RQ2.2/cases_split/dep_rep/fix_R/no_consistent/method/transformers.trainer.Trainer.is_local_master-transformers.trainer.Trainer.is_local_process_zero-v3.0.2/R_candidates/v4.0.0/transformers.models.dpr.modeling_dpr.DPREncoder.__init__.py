    def __init__(self, config: DPRConfig):
        super().__init__(config)
        self.bert_model = BertModel(config)
        assert self.bert_model.config.hidden_size > 0, "Encoder hidden_size can't be zero"
        self.projection_dim = config.projection_dim
        if self.projection_dim > 0:
            self.encode_proj = nn.Linear(self.bert_model.config.hidden_size, config.projection_dim)
        self.init_weights()
