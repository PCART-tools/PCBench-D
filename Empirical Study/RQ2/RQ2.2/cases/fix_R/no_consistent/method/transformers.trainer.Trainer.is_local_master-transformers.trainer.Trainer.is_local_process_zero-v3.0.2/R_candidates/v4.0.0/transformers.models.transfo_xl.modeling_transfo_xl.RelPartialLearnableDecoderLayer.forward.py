    def forward(self, dec_inp, r, dec_attn_mask=None, mems=None, head_mask=None, output_attentions=False):

        attn_outputs = self.dec_attn(
            dec_inp,
            r,
            attn_mask=dec_attn_mask,
            mems=mems,
            head_mask=head_mask,
            output_attentions=output_attentions,
        )
        ff_output = self.pos_ff(attn_outputs[0])

        outputs = [ff_output] + attn_outputs[1:]

        return outputs
