    def call(self, inputs):
        hidden_states = self.dense(inputs)
        hidden_states = self.LayerNorm(hidden_states)
        return hidden_states
