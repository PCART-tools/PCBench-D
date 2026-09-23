    def call(self, hidden_states, attention_mask, head_mask, output_attentions, training=False):
        attention_outputs = self.attention(
            hidden_states, attention_mask, head_mask, output_attentions, training=training
        )
        ffn_output = self.ffn(attention_outputs[0])
        ffn_output = self.activation(ffn_output)
        ffn_output = self.ffn_output(ffn_output)
        ffn_output = self.dropout(ffn_output, training=training)

        hidden_states = self.full_layer_layer_norm(ffn_output + attention_outputs[0])

        # add attentions if we output them
        outputs = (hidden_states,) + attention_outputs[1:]
        return outputs
