    @nn.compact
    def __call__(self, inputs, attention_mask):
        assert self.num_layers > 0, f"num_layers should be >= 1, got ({self.num_layers})"

        # Initialize input / output
        input_i = inputs

        # Forward over all encoders
        for i in range(self.num_layers):
            layer = FlaxBertLayer(self.num_heads, self.head_size, self.intermediate_size, name=f"{i}")
            input_i = layer(input_i, attention_mask)
        return input_i
