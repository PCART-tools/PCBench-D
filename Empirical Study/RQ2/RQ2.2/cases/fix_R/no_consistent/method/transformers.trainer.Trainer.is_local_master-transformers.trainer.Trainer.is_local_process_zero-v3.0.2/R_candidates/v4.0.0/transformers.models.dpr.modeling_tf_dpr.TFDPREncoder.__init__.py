    def __init__(self, config: DPRConfig, *args, **kwargs):
        super().__init__(config, *args, **kwargs)

        # resolve name conflict with TFBertMainLayer instead of TFBertModel
        self.bert_model = TFBertMainLayer(config, name="bert_model")
        self.bert_model.config = config

        assert self.bert_model.config.hidden_size > 0, "Encoder hidden_size can't be zero"
        self.projection_dim = config.projection_dim
        if self.projection_dim > 0:
            self.encode_proj = Dense(
                config.projection_dim, kernel_initializer=get_initializer(config.initializer_range), name="encode_proj"
            )
