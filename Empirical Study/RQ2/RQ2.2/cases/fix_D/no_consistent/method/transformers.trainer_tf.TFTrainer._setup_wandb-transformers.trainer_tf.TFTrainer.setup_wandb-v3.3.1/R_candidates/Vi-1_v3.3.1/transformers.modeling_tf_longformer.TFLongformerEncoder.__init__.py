    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.output_hidden_states = config.output_hidden_states
        self.output_attentions = config.output_attentions
        self.layer = [
            TFLongformerLayer(config, i, name="layer_._{}".format(i)) for i in range(config.num_hidden_layers)
        ]
