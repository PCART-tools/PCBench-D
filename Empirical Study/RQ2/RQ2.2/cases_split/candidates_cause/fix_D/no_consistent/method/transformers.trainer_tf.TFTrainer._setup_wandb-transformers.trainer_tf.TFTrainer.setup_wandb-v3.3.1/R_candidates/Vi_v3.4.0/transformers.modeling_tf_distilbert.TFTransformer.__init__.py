    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.n_layers = config.n_layers
        self.output_hidden_states = config.output_hidden_states
        self.output_attentions = config.output_attentions

        self.layer = [TFTransformerBlock(config, name="layer_._{}".format(i)) for i in range(config.n_layers)]
