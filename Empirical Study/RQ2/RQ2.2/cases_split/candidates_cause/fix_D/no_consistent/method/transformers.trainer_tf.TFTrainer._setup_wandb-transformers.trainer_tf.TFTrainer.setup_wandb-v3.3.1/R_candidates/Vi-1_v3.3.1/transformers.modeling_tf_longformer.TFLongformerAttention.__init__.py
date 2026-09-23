    def __init__(self, config, layer_id=0, **kwargs):
        super().__init__(**kwargs)

        self.self_attention = TFLongformerSelfAttention(config, layer_id, name="self")
        self.dense_output = TFLongformerSelfOutput(config, name="output")
