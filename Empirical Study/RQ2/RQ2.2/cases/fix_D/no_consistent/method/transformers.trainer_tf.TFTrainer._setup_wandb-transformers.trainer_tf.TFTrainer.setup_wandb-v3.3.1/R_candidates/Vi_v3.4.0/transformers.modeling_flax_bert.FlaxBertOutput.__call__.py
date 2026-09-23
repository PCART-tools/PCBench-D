    @compact
    def __call__(self, intermediate_output, attention_output):
        hidden_state = nn.Dense(attention_output.shape[-1], name="dense")(intermediate_output)
        hidden_state = FlaxBertLayerNorm(name="layer_norm")(hidden_state + attention_output)
        return hidden_state
