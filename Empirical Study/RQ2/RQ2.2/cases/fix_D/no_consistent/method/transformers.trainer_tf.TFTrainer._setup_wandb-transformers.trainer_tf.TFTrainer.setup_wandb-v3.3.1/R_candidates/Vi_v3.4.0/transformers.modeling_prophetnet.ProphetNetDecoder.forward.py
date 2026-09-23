    @add_start_docstrings_to_callable(PROPHETNET_STANDALONE_INPUTS_DOCSTRING)
    @replace_return_docstrings(output_type=ProphetNetDecoderModelOutput, config_class=_CONFIG_FOR_DOC)
    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        encoder_hidden_states=None,
        encoder_attention_mask=None,
        past_key_values=None,
        inputs_embeds=None,
        use_cache=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
    ):
        r"""
        encoder_hidden_states  (:obj:`torch.FloatTensor` of shape :obj:`(batch_size, sequence_length, hidden_size)`, `optional`):
            Sequence of hidden-states at the output of the last layer of the encoder. Used in the cross-attention
            if the model is configured as a decoder.
        encoder_attention_mask (:obj:`torch.FloatTensor` of shape :obj:`(batch_size, sequence_length)`, `optional`):
            Mask to avoid performing attention on the padding token indices of the encoder input. This mask
            is used in the cross-attention if the model is configured as a decoder.
            Mask values selected in ``[0, 1]``:
        past_key_values (:obj:`tuple(tuple(torch.FloatTensor))` of length :obj:`config.n_layers` with each tuple having 4 tensors of shape :obj:`(batch_size, num_heads, sequence_length - 1, embed_size_per_head)`):
            Contains precomputed key and value hidden-states of the attention blocks. Can be used to speed up decoding.

            If :obj:`past_key_values` are used, the user can optionally input only the last
            ``decoder_input_ids`` (those that don't have their past key value states given to this model) of shape
            :obj:`(batch_size, 1)` instead of all ``decoder_input_ids`` of shape :obj:`(batch_size, sequence_length)`.
        use_cache (:obj:`bool`, `optional`):
            If set to :obj:`True`, :obj:`past_key_values` key value states are returned and can be used to speed up
            decoding (see :obj:`past_key_values`).

            - 1 for tokens that are **not masked**,
            - 0 for tokens that are **masked**.

        Returns:

        Example::

            >>> from transformers import ProphetNetTokenizer, ProphetNetDecoder
            >>> import torch

            >>> tokenizer = ProphetNetTokenizer.from_pretrained('microsoft/prophetnet-large-uncased')
            >>> model = ProphetNetDecoder.from_pretrained('patrickvonplaten/prophetnet-large-uncased-standalone', add_cross_attention=False, return_dict=True)
            >>> assert model.config.is_decoder, f"{model.__class__} has to be configured as a decoder."
            >>> inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
            >>> outputs = model(**inputs)

            >>> last_hidden_states = outputs.last_hidden_state
        """
        use_cache = use_cache if use_cache is not None else self.config.use_cache
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        if input_ids is None and inputs_embeds is None:
            raise ValueError("Either `decoder_input_ids` or `decoder_inputs_embeds` has to be passed.")
        elif input_ids is not None and inputs_embeds is not None:
            raise ValueError("Make sure to only pass `decoder_input_ids` or `decoder_inputs_embeds`.")
        elif input_ids is not None and inputs_embeds is None:
            inputs_embeds = self.word_embeddings(input_ids)

        batch_size, sequence_length = inputs_embeds.shape[:2]

        main_stream_pos_embed, position_ids = self.position_embeddings(
            (batch_size, sequence_length),
            device=inputs_embeds.device,
            past_key_values=past_key_values,
        )

        if past_key_values is not None:
            main_relative_position_buckets, predict_relative_position_buckets = None, None
        else:
            (
                main_relative_position_buckets,
                predict_relative_position_buckets,
            ) = self.compute_buffered_relative_buckets(position_ids)
        predicting_stream_pos_embed = self.position_embeddings._forward(position_ids + 1)

        # add position embeddings
        hidden_states = inputs_embeds + main_stream_pos_embed
        hidden_states = hidden_states.transpose(0, 1)

        ngram_embeddings = self.ngram_embeddings.weight

        # prepare attention mask
        if past_key_values is not None:
            assert (
                hidden_states.size(0) == 1
            ), "At the moment `use_cache` is only supported for `decoder_input_ids` of length 1"

            ngram_hidden_states = [
                (ngram_embeddings[ngram - 1] + predicting_stream_pos_embed).transpose(0, 1).repeat(1, batch_size, 1)
                for ngram in range(self.ngram)
            ]
            extended_attention_mask = None
            extended_predict_attention_mask = None
        else:
            ngram_hidden_states = [
                (ngram_embeddings[ngram - 1] + predicting_stream_pos_embed).transpose(0, 1)
                for ngram in range(self.ngram)
            ]
            extended_attention_mask = self.prepare_attention_mask(hidden_states, attention_mask)
            extended_predict_attention_mask = self.prepare_predict_attention_mask(hidden_states, attention_mask)

        # prepare encoder attention mask
        if encoder_attention_mask is not None:
            extended_encoder_attention_mask = (
                1.0 - encoder_attention_mask[:, None, :].repeat(self.config.num_attention_heads, 1, 1)
            ) * -10000.0
            extended_encoder_attention_mask = extended_encoder_attention_mask.to(inputs_embeds.dtype)
        else:
            extended_encoder_attention_mask = None

        hidden_states = torch.cat([hidden_states] + ngram_hidden_states, 0)

        if self.embeddings_layer_norm:
            hidden_states = self.embeddings_layer_norm(hidden_states)

        hidden_states = F.dropout(hidden_states, p=self.dropout, training=self.training)

        if encoder_hidden_states is not None:
            encoder_hidden_states = encoder_hidden_states.transpose(0, 1)

        # init attentions, hidden_states and cache with empty tuples
        all_main_stream_hidden_states = () if output_hidden_states else None
        all_ngram_stream_hidden_states = () if output_hidden_states and self.config.ngram > 0 else None

        all_main_stream_attns = () if output_attentions else None
        all_ngram_stream_attns = () if output_attentions else None
        all_cross_attns = () if output_attentions and self.config.add_cross_attention else None
        present_key_values = () if use_cache else None

        for idx, decoder_layer in enumerate(self.layers):
            if output_hidden_states:
                all_main_stream_hidden_states += (hidden_states[:sequence_length].transpose(0, 1),)
                if self.config.ngram > 0:
                    all_ngram_stream_hidden_states += (hidden_states[sequence_length:].transpose(0, 1),)

            layer_state = past_key_values[idx] if past_key_values is not None else None
            (
                hidden_states,
                layer_self_attn,
                layer_self_predict_attn_output,
                layer_cross_attn,
                layer_past,
            ) = decoder_layer(
                hidden_states,
                encoder_hidden_states=encoder_hidden_states,
                encoder_attn_mask=extended_encoder_attention_mask,
                layer_state=layer_state,
                attention_mask=extended_attention_mask,
                extended_predict_attention_mask=extended_predict_attention_mask,
                main_relative_position_buckets=main_relative_position_buckets,
                predict_relative_position_buckets=predict_relative_position_buckets,
                position_ids=position_ids,
            )
            if use_cache:
                present_key_values += (layer_past,)

            if output_attentions:
                all_main_stream_attns += (layer_self_attn,)
                all_ngram_stream_attns += (layer_self_predict_attn_output,)

                if self.config.add_cross_attention:
                    all_cross_attns += (layer_cross_attn,)

        if output_hidden_states:
            all_main_stream_hidden_states += (hidden_states[:sequence_length].transpose(0, 1),)
            if self.config.ngram > 0:
                all_ngram_stream_hidden_states += (hidden_states[sequence_length:].transpose(0, 1),)

        # split last_hidden_state for return
        last_hidden_state = hidden_states[:sequence_length].transpose(0, 1)
        last_hidden_state_ngram = hidden_states[sequence_length:].transpose(0, 1) if self.config.ngram > 0 else None
        encoder_hidden_states = encoder_hidden_states.transpose(0, 1) if encoder_hidden_states is not None else None

        if not return_dict:
            return tuple(
                v
                for v in [
                    last_hidden_state,
                    last_hidden_state_ngram,
                    present_key_values,
                    all_main_stream_hidden_states,
                    all_ngram_stream_hidden_states,
                    all_main_stream_attns,
                    all_ngram_stream_attns,
                    all_cross_attns,
                ]
                if v is not None
            )
        return ProphetNetDecoderModelOutput(
            last_hidden_state=last_hidden_state,
            last_hidden_state_ngram=last_hidden_state_ngram,
            past_key_values=present_key_values,
            hidden_states=all_main_stream_hidden_states,
            hidden_states_ngram=all_ngram_stream_hidden_states,
            attentions=all_main_stream_attns,
            ngram_attentions=all_ngram_stream_attns,
            cross_attentions=all_cross_attns,
        )
