    def call(self, hidden, training=False):
        hidden = self.linear_hidden(hidden)
        hidden = tf.keras.activations.tanh(hidden)
        hidden = self.dropout(hidden, training=training)
        return self.linear_out(hidden)
