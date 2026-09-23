    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.visual_attention = TFLxmertCrossAttentionLayer(config, name="visual_attention")

        # Self-attention Layers
        self.lang_self_att = TFLxmertSelfAttentionLayer(config, name="lang_self_att")
        self.visn_self_att = TFLxmertSelfAttentionLayer(config, name="visn_self_att")

        # Intermediate and Output Layers (FFNs)
        self.lang_inter = TFLxmertIntermediate(config, name="lang_inter")
        self.lang_output = TFLxmertOutput(config, name="lang_output")
        self.visn_inter = TFLxmertIntermediate(config, name="visn_inter")
        self.visn_output = TFLxmertOutput(config, name="visn_output")
