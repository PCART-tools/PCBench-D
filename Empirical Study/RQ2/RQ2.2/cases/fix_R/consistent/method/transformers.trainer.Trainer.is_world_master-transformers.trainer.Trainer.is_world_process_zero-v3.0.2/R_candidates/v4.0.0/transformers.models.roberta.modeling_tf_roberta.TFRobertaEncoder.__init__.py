    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.layer = [TFRobertaLayer(config, name="layer_._{}".format(i)) for i in range(config.num_hidden_layers)]
