    def call(
        self,
        input_ids=None,
        attention_mask=None,
        output_attentions=False,
        output_hidden_states=False,
        return_dict=None,
        training=False,
    ):
        """
        Args:
            input_ids (Tensor): tokens in the source language of shape
                `(batch, src_len)`
            attention_mask (Tensor): indicating which indices are padding tokens

        Returns:
            namedtuple:

                - **x** (Tensor): the last encoder layer's output of shape `(src_len, batch, embed_dim)`

                - **encoder_states** (List[Tensor]): all intermediate hidden states of shape `(src_len, batch,
                  embed_dim)`. Only populated if *output_hidden_states* is True.
                - **all_attentions** (List[Tensor]): Attention weights for each layer.
                During training might not be of length n_layers because of layer dropout.
        """
        output_attentions = output_attentions if output_attentions is not None else self.output_attentions
        output_hidden_states = output_hidden_states if output_hidden_states is not None else self.output_hidden_states
        return_dict = return_dict if return_dict is not None else self.return_dict

        # check attention mask and invert
        if attention_mask is not None:
            assert (
                attention_mask._rank() == 2
            ), f"expected attention_mask._rank() to be a 2D tensor got {attention_mask._rank()}"
            attention_mask = tf.cast(attention_mask, dtype=tf.float32)
            attention_mask = (1.0 - attention_mask) * LARGE_NEGATIVE
        inputs_embeds = self.embed_tokens(input_ids) * self.embed_scale
        embed_pos = self.embed_positions(input_ids)
        x = inputs_embeds + embed_pos
        x = self.layernorm_embedding(x)
        x = tf.nn.dropout(x, rate=self.dropout if training else 0)

        # B x T x C -> T x B x C
        x = tf.transpose(x, perm=[1, 0, 2])

        encoder_states = [] if output_hidden_states else None
        all_attentions = () if output_attentions else None

        # encoder layers
        for encoder_layer in self.layers:

            if output_hidden_states:
                encoder_states.append(x)
            # add LayerDrop (see https://arxiv.org/abs/1909.11556 for description)
            dropout_probability = random.uniform(0, 1)
            if training and (dropout_probability < self.layerdrop):  # skip the layer
                attn = None
            else:
                x, attn = encoder_layer(x, attention_mask)

            if output_attentions:
                all_attentions += (attn,)
        if self.layer_norm:
            x = self.layer_norm(x)
        if output_hidden_states:
            encoder_states.append(x)
            encoder_states = [tf.transpose(hidden_state, perm=(1, 0, 2)) for hidden_state in encoder_states]
        x = tf.transpose(x, perm=(1, 0, 2))
        if not return_dict:
            return tuple(v for v in [x, encoder_states, all_attentions] if v is not None)
        return TFBaseModelOutput(last_hidden_state=x, hidden_states=encoder_states, attentions=all_attentions)
