    @compact
    def __call__(self, hidden_state, attention_mask):
        attention = FlaxRobertaAttention(self.num_heads, self.head_size, name="attention")(
            hidden_state, attention_mask
        )
        intermediate = FlaxRobertaIntermediate(self.intermediate_size, name="intermediate")(attention)
        output = FlaxRobertaOutput(name="output")(intermediate, attention)

        return output
