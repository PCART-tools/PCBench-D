    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.attention = TFElectraAttention(config, name="attention")
        self.intermediate = TFElectraIntermediate(config, name="intermediate")
        self.bert_output = TFElectraOutput(config, name="output")
