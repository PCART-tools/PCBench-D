    @nn.compact
    def __call__(self, hidden_state, attention_mask):
        layer = FlaxBertLayerCollection(
            self.num_layers, self.num_heads, self.head_size, self.intermediate_size, name="layer"
        )(hidden_state, attention_mask)
        return layer
