    def call(self, hidden_states, residual_tensor_1, residual_tensor_2, training=False):
        hidden_states = self.dense(hidden_states)
        if not self.use_bottleneck:
            hidden_states = self.dropout(hidden_states, training=training)
            hidden_states = self.LayerNorm(hidden_states + residual_tensor_1)
        else:
            hidden_states = self.LayerNorm(hidden_states + residual_tensor_1)
            hidden_states = self.bottleneck(hidden_states, residual_tensor_2)
        return hidden_states
