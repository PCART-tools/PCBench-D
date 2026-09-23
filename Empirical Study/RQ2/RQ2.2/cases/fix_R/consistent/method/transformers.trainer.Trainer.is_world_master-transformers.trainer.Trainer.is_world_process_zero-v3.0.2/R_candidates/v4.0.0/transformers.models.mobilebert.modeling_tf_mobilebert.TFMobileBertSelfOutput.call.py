    def call(self, hidden_states, residual_tensor, training=False):
        hidden_states = self.dense(hidden_states)
        if not self.use_bottleneck:
            hidden_states = self.dropout(hidden_states, training=training)
        hidden_states = self.LayerNorm(hidden_states + residual_tensor)
        return hidden_states
