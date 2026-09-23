    def __init__(self, config, has_relative_attention_bias=False, **kwargs):
        super().__init__(**kwargs)
        self.is_decoder = config.is_decoder
        self.layer = []
        self.layer.append(
            TFT5LayerSelfAttention(
                config,
                has_relative_attention_bias=has_relative_attention_bias,
                name="layer_._0",
            )
        )
        if self.is_decoder:
            self.layer.append(
                TFT5LayerCrossAttention(
                    config,
                    name="layer_._1",
                )
            )

        self.layer.append(TFT5LayerFF(config, name="layer_._{}".format(len(self.layer))))
