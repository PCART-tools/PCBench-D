    def __init__(self, config, layer_id=0):
        super().__init__()
        self.attention = LongformerAttention(config, layer_id)
        self.intermediate = LongformerIntermediate(config)
        self.output = LongformerOutput(config)
        self.chunk_size_feed_forward = config.chunk_size_feed_forward
        self.seq_len_dim = 1
