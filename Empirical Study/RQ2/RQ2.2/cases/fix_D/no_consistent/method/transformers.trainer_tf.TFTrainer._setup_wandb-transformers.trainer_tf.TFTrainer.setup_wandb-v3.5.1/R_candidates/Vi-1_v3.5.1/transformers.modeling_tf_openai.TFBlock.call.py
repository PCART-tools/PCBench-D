    def call(self, x, attention_mask, head_mask, output_attentions, training=False):
        output_attn = self.attn(x, attention_mask, head_mask, output_attentions, training=training)
        a = output_attn[0]  # output_attn: a, (attentions)

        n = self.ln_1(x + a)
        m = self.mlp(n, training=training)
        h = self.ln_2(n + m)

        outputs = [h] + output_attn[1:]
        return outputs  # x, (attentions)
