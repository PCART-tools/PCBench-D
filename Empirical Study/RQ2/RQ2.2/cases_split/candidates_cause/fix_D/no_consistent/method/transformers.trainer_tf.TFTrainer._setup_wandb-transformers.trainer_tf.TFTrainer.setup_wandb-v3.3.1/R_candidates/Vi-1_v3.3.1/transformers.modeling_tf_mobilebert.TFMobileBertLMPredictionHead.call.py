    def call(self, hidden_states):
        hidden_states = self.transform(hidden_states)
        hidden_states = tf.matmul(hidden_states, tf.concat([tf.transpose(self.decoder), self.dense], axis=0))
        hidden_states = hidden_states + self.bias
        return hidden_states
