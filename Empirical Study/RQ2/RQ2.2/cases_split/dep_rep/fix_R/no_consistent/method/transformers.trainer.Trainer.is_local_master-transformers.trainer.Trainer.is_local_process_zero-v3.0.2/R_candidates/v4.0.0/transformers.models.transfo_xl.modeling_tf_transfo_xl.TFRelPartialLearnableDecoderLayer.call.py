    def call(self, dec_inp, r, dec_attn_mask, mems, head_mask, output_attentions, training=False):
        attn_outputs = self.dec_attn(dec_inp, r, dec_attn_mask, mems, head_mask, output_attentions, training=training)
        ff_output = self.pos_ff(attn_outputs[0], training=training)

        outputs = [ff_output] + attn_outputs[1:]

        return outputs
