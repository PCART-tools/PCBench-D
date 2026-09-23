    def call(
        self,
        lang_feats,
        lang_attention_mask,
        visn_feats,
        visn_attention_mask,
        output_attentions,
        training=False,
    ):
        lang_att_output = lang_feats
        visn_att_output = visn_feats

        lang_att_output, visn_att_output = self.cross_att(
            lang_att_output,
            lang_attention_mask,
            visn_att_output,
            visn_attention_mask,
            output_attentions,
            training=training,
        )
        attention_probs = lang_att_output[1:]
        lang_att_output, visn_att_output = self.self_att(
            lang_att_output[0],
            lang_attention_mask,
            visn_att_output[0],
            visn_attention_mask,
            training=training,
        )
        lang_output, visn_output = self.output_fc(lang_att_output, visn_att_output, training=training)

        return (lang_output, visn_output, attention_probs[0]) if output_attentions else (lang_output, visn_output)
