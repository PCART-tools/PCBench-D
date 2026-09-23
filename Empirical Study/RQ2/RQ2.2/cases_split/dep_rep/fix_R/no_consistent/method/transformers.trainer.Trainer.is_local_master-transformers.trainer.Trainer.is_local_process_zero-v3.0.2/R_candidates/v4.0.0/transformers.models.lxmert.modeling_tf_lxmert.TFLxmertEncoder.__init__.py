    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.visn_fc = TFLxmertVisualFeatureEncoder(config, name="visn_fc")

        # Number of layers
        self.num_l_layers = config.l_layers
        self.num_x_layers = config.x_layers
        self.num_r_layers = config.r_layers

        # Layers
        # Using self.layer instead of self.l_layer to support loading BERT weights.
        self.layer = [TFLxmertLayer(config, name="layer_._{}".format(i)) for i in range(self.num_l_layers)]
        self.x_layers = [TFLxmertXLayer(config, name="x_layers_._{}".format(i)) for i in range(self.num_x_layers)]
        self.r_layers = [TFLxmertLayer(config, name="r_layers_._{}".format(i)) for i in range(self.num_r_layers)]
        self.config = config
