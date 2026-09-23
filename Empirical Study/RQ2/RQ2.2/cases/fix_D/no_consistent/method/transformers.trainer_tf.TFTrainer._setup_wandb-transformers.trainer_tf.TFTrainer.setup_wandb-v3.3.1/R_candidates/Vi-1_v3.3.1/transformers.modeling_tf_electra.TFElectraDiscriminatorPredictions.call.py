    def call(self, discriminator_hidden_states, training=False):
        hidden_states = self.dense(discriminator_hidden_states)
        hidden_states = get_tf_activation(self.config.hidden_act)(hidden_states)
        logits = tf.squeeze(self.dense_prediction(hidden_states))

        return logits
