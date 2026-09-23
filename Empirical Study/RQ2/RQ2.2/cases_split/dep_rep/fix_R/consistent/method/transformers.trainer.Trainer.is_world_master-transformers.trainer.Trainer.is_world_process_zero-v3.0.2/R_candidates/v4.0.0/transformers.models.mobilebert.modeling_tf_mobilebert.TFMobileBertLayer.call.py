    def call(self, hidden_states, attention_mask, head_mask, output_attentions, training=False):
        if self.use_bottleneck:
            query_tensor, key_tensor, value_tensor, layer_input = self.bottleneck(hidden_states)
        else:
            query_tensor, key_tensor, value_tensor, layer_input = [hidden_states] * 4

        attention_outputs = self.attention(
            query_tensor,
            key_tensor,
            value_tensor,
            layer_input,
            attention_mask,
            head_mask,
            output_attentions,
            training=training,
        )

        attention_output = attention_outputs[0]
        s = (attention_output,)

        if self.num_feedforward_networks != 1:
            for i, ffn_module in enumerate(self.ffn):
                attention_output = ffn_module(attention_output)
                s += (attention_output,)

        intermediate_output = self.intermediate(attention_output)
        layer_output = self.mobilebert_output(intermediate_output, attention_output, hidden_states, training=training)

        outputs = (
            (layer_output,)
            + attention_outputs[1:]
            + (
                tf.constant(0),
                query_tensor,
                key_tensor,
                value_tensor,
                layer_input,
                attention_output,
                intermediate_output,
            )
            + s
        )  # add attentions if we output them

        return outputs
