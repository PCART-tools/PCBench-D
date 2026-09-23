    @compact
    def __call__(self, hidden_state, attention_mask):
        attention = FlaxBertAttention(self.num_heads, self.head_size, name="attention")(hidden_state, attention_mask)
        intermediate = FlaxBertIntermediate(self.intermediate_size, name="intermediate")(attention)
        output = FlaxBertOutput(name="output")(intermediate, attention)

        return output
