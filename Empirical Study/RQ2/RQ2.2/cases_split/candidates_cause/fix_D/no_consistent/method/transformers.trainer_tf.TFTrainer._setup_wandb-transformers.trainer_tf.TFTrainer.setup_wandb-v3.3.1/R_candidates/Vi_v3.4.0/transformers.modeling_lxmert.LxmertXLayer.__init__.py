    def __init__(self, config):
        super().__init__()
        # The cross-attention Layer
        self.visual_attention = LxmertCrossAttentionLayer(config)

        # Self-attention Layers
        self.lang_self_att = LxmertSelfAttentionLayer(config)
        self.visn_self_att = LxmertSelfAttentionLayer(config)

        # Intermediate and Output Layers (FFNs)
        self.lang_inter = LxmertIntermediate(config)
        self.lang_output = LxmertOutput(config)
        self.visn_inter = LxmertIntermediate(config)
        self.visn_output = LxmertOutput(config)
