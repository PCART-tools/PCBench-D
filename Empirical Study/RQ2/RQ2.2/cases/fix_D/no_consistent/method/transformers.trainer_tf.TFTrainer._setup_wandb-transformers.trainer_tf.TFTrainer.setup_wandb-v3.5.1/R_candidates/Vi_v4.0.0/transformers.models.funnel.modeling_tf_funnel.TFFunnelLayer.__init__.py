    def __init__(self, config, block_index, **kwargs):
        super().__init__(**kwargs)
        self.attention = TFFunnelRelMultiheadAttention(config, block_index, name="attention")
        self.ffn = TFFunnelPositionwiseFFN(config, name="ffn")
