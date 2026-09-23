    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.attention = TFRobertaAttention(config, name="attention")
        self.intermediate = TFRobertaIntermediate(config, name="intermediate")
        self.bert_output = TFRobertaOutput(config, name="output")
