    def call(self, inputs, training=False):
        (
            hidden_states,
            attention_mask,
            is_index_masked,
            is_index_global_attn,
            is_global_attn,
        ) = inputs

        attention_outputs = self.attention(
            [hidden_states, attention_mask, is_index_masked, is_index_global_attn, is_global_attn],
            training=training,
        )
        attention_output = attention_outputs[0]
        intermediate_output = self.intermediate(attention_output)
        layer_output = self.longformer_output(intermediate_output, attention_output, training=training)
        outputs = (layer_output,) + attention_outputs[1:]  # add attentions if we output them

        return outputs
