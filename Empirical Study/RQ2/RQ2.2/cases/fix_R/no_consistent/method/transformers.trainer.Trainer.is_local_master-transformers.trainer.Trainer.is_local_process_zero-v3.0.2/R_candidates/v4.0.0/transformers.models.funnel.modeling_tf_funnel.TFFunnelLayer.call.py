    def call(self, query, key, value, attention_inputs, output_attentions=False, training=False):
        attn = self.attention(
            query, key, value, attention_inputs, output_attentions=output_attentions, training=training
        )
        output = self.ffn(attn[0], training=training)
        return (output, attn[1]) if output_attentions else (output,)
