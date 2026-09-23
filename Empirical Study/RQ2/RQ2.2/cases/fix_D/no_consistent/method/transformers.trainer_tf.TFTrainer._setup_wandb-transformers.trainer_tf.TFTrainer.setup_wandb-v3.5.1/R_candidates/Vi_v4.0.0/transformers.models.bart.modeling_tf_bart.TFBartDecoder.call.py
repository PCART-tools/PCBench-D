    def call(
        self,
        input_ids,
        encoder_hidden_states,
        encoder_padding_mask,
        decoder_padding_mask,
        decoder_causal_mask,
        decoder_cached_states=None,
        use_cache=False,
        output_attentions=False,
        output_hidden_states=False,
        return_dict=None,
        training=False,
    ):
        output_attentions = output_attentions if output_attentions is not None else self.output_attentions
        output_hidden_states = output_hidden_states if output_hidden_states is not None else self.output_hidden_states
        use_cache = use_cache if use_cache is not None else self.use_cache
        return_dict = return_dict if return_dict is not None else self.config.return_dict
        if use_cache:
            assert not training, "Training + use cache are incompatible"
        # check attention mask and invert
        use_cache = cast_bool_to_primitive(use_cache)
        if encoder_padding_mask is not None:
            encoder_padding_mask = invert_mask(encoder_padding_mask)

        # embed positions
        positions = self.embed_positions(input_ids, use_cache=use_cache)

        if use_cache:
            input_ids = input_ids[:, -1:]
            positions = positions[:, -1:]

        x = self.embed_tokens(input_ids) * self.embed_scale
        if self.do_blenderbot_90_layernorm:
            x = self.layernorm_embedding(x) + positions
        else:
            x = self.layernorm_embedding(x + positions)
        x = tf.nn.dropout(x, rate=self.dropout if training else 0)

        # Convert to Bart output format: (BS, seq_len, model_dim) ->  (seq_len, BS, model_dim)
        x = tf.transpose(x, perm=(1, 0, 2))
        assert len(shape_list(encoder_hidden_states)) == 3, "encoder_hidden_states must be a 3D tensor"
        encoder_hidden_states = tf.transpose(encoder_hidden_states, perm=(1, 0, 2))

        # decoder layers
        all_hidden_states = ()
        all_self_attns = ()
        next_decoder_cache = []
        for idx, decoder_layer in enumerate(self.layers):
            # add LayerDrop (see https://arxiv.org/abs/1909.11556 for description)
            if output_hidden_states:
                all_hidden_states += (x,)
            dropout_probability = random.uniform(0, 1)
            if training and (dropout_probability < self.layerdrop):
                continue

            layer_state = decoder_cached_states[idx] if decoder_cached_states is not None else None

            x, layer_self_attn, layer_past = decoder_layer(
                x,
                encoder_hidden_states,
                encoder_attn_mask=encoder_padding_mask,
                decoder_padding_mask=decoder_padding_mask,
                layer_state=layer_state,
                causal_mask=decoder_causal_mask,
            )

            if use_cache:
                next_decoder_cache.append(layer_past.copy())

            if output_attentions:
                all_self_attns += (layer_self_attn,)

        if self.layer_norm is not None:  # same as if config.add_final_layer_norm
            x = self.layer_norm(x)

        # Convert to standard output format: (seq_len, BS, model_dim) -> (BS, seq_len, model_dim)
        if output_hidden_states:
            all_hidden_states += (x,)
            # T x B x C -> B x T x C
            all_hidden_states = tuple(tf.transpose(hs, perm=(1, 0, 2)) for hs in all_hidden_states)
        else:
            all_hidden_states = None
        all_self_attns = list(all_self_attns) if output_attentions else None

        x = tf.transpose(x, perm=(1, 0, 2))
        encoder_hidden_states = tf.transpose(encoder_hidden_states, perm=(1, 0, 2))  # could maybe be avoided.

        next_cache = (encoder_hidden_states, next_decoder_cache) if use_cache else None
        if not return_dict:
            return x, next_cache, all_hidden_states, all_self_attns
        else:
            return TFBaseModelOutputWithPast(
                last_hidden_state=x,
                past_key_values=next_cache,
                hidden_states=all_hidden_states,
                attentions=all_self_attns,
            )
