    def call(self, inputs, training=False):
        (
            hidden_states,
            attention_mask,
            is_index_masked,
            is_index_global_attn,
            is_global_attn,
            output_attentions,
        ) = inputs

        self_outputs = self.self_attention(
            [hidden_states, attention_mask, is_index_masked, is_index_global_attn, is_global_attn, output_attentions],
            training=training,
        )
        attention_output = self.dense_output(self_outputs[0], hidden_states, training=training)
        outputs = (attention_output,) + self_outputs[1:]

        return outputs
