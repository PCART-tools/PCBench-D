    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.output_attentions = config.output_attentions
        self.output_hidden_states = config.output_hidden_states
        self.albert_layers = [
            TFAlbertLayer(config, name="albert_layers_._{}".format(i)) for i in range(config.inner_group_num)
        ]
