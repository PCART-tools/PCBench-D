    def call(
        self,
        output_h,
        output_g,
        non_tgt_mask,
        attn_mask,
        pos_emb,
        seg_mat,
        mems,
        target_mapping,
        head_mask,
        output_attentions,
        training=False,
    ):
        outputs = self.rel_attn(
            output_h,
            output_g,
            non_tgt_mask,
            attn_mask,
            pos_emb,
            seg_mat,
            mems,
            target_mapping,
            head_mask,
            output_attentions,
            training=training,
        )
        output_h, output_g = outputs[:2]

        if output_g is not None:
            output_g = self.ff(output_g, training=training)
        output_h = self.ff(output_h, training=training)

        outputs = (output_h, output_g) + outputs[2:]  # Add again attentions if there are there
        return outputs
