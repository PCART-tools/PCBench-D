    def call(self, hidden_states, training=False):
        norm_x = self.layer_norm(hidden_states)
        y = self.DenseReluDense(norm_x, training=training)
        layer_output = hidden_states + self.dropout(y, training=training)
        return layer_output
