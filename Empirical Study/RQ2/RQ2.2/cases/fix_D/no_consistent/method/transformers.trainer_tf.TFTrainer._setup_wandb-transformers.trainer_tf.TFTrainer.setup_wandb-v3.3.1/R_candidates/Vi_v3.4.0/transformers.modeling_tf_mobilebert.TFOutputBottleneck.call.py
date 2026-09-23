    def call(self, hidden_states, residual_tensor, training=False):
        layer_outputs = self.dense(hidden_states)
        layer_outputs = self.dropout(layer_outputs, training=training)
        layer_outputs = self.LayerNorm(layer_outputs + residual_tensor)
        return layer_outputs
