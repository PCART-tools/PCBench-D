    def call(
        self,
        hidden_states,
        attention_mask=None,
        position_bias=None,
        head_mask=None,
        past_key_value_state=None,
        use_cache=False,
        output_attentions=False,
        training=False,
    ):
        norm_x = self.layer_norm(hidden_states)
        attention_output = self.SelfAttention(
            norm_x,
            mask=attention_mask,
            position_bias=position_bias,
            head_mask=head_mask,
            past_key_value_state=past_key_value_state,
            use_cache=use_cache,
            output_attentions=output_attentions,
            training=training,
        )
        y = attention_output[0]
        layer_output = hidden_states + self.dropout(y, training=training)
        outputs = (layer_output,) + attention_output[1:]  # add attentions if we output them
        return outputs
