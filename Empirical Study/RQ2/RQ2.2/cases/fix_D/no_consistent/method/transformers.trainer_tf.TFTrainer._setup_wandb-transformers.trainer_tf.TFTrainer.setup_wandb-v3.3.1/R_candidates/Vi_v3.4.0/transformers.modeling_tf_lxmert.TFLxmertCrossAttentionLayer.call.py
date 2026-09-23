    def call(
        self,
        input_tensor,
        ctx_tensor,
        ctx_att_mask,
        output_attentions=False,
        training=False,
    ):
        output = self.att(input_tensor, ctx_tensor, ctx_att_mask, output_attentions, training=training)
        if output_attentions:
            attention_probs = output[1]
        attention_output = self.attention_output(output[0], input_tensor, training=training)
        outputs = (attention_output, attention_probs) if output_attentions else (attention_output,)
        return outputs
