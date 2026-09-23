    def forward(
        self,
        hidden_states,
        encoder_hidden_states=None,
        encoder_attn_mask=None,
        layer_state=None,
        attention_mask=None,
        extended_predict_attention_mask=None,
        main_relative_position_buckets=None,
        predict_relative_position_buckets=None,
        position_ids=None,
    ):
        layer_state = layer_state if layer_state is not None else {}

        # 1st residual block
        ngram_attention_output, self_attn_weights, self_attn_weights_ngram = self.self_attn(
            hidden_states=hidden_states,
            layer_state=layer_state,
            attention_mask=attention_mask,
            extended_predict_attention_mask=extended_predict_attention_mask,
            main_relative_position_buckets=main_relative_position_buckets,
            predict_relative_position_buckets=predict_relative_position_buckets,
            position_ids=position_ids,
        )
        hidden_states = self.self_attn_layer_norm(hidden_states + ngram_attention_output)

        cross_attn_weights = None
        if encoder_hidden_states is not None:
            # 2nd residual block
            attention_output, cross_attn_weights = self.cross_attn(
                hidden_states=hidden_states,
                key_value_states=encoder_hidden_states,
                attention_mask=encoder_attn_mask,
                layer_state=layer_state,  # mutates layer state
            )
            hidden_states = self.cross_attn_layer_norm(attention_output + hidden_states)

        # 3rd residual block
        feed_forward_output = self.feed_forward(hidden_states)
        hidden_states = self.feed_forward_layer_norm(feed_forward_output + hidden_states)

        return (
            hidden_states,
            self_attn_weights,
            self_attn_weights_ngram,
            cross_attn_weights,
            layer_state,
        )  # just self_attn weights for now, following t5, layer_state = cache for decoding
