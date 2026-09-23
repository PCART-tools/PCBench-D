    def __init__(self, config, layer_id=0, **kwargs):
        super().__init__(**kwargs)

        self.attention = TFLongformerAttention(config, layer_id, name="attention")
        self.intermediate = TFLongformerIntermediate(config, name="intermediate")
        self.longformer_output = TFLongformerOutput(config, name="output")
