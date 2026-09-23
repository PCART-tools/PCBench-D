    def call(
        self,
        query_tensor,
        key_tensor,
        value_tensor,
        layer_input,
        attention_mask,
        head_mask,
        output_attentions,
        training=False,
    ):
        self_outputs = self.self(
            query_tensor, key_tensor, value_tensor, attention_mask, head_mask, output_attentions, training=training
        )

        attention_output = self.mobilebert_output(self_outputs[0], layer_input, training=training)
        outputs = (attention_output,) + self_outputs[1:]  # add attentions if we output them
        return outputs
