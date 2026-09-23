    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.output_attentions = config.output_attentions
        self.output_hidden_states = config.output_hidden_states
        self.layer = [TFMobileBertLayer(config, name="layer_._{}".format(i)) for i in range(config.num_hidden_layers)]
