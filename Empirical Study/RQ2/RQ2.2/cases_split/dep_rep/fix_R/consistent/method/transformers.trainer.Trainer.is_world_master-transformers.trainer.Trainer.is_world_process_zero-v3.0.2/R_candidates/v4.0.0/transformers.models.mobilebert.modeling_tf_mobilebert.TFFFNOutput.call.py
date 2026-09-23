    def call(self, hidden_states, residual_tensor):
        hidden_states = self.dense(hidden_states)
        hidden_states = self.LayerNorm(hidden_states + residual_tensor)
        return hidden_states
