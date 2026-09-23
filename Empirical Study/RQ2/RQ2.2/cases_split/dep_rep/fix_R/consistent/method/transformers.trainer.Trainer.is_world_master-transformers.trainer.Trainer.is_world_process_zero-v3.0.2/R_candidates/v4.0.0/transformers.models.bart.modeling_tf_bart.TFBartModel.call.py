    @add_start_docstrings_to_model_forward(BART_INPUTS_DOCSTRING)
    @replace_return_docstrings(output_type=TFSeq2SeqModelOutput, config_class=_CONFIG_FOR_DOC)
    def call(
        self,
        inputs,
        attention_mask=None,
        decoder_input_ids=None,  # BAD DEFAULT LEFT FOR CONSISTENT SIGNATURE
        decoder_attention_mask=None,
        encoder_outputs: Optional[TFBaseModelOutput] = None,
        past_key_values=None,
        use_cache=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
        training=False,
        **kwargs
    ):
        """
        Returns:
        """
        assert "decoder_cached_states" not in kwargs, "Please use past_key_values to cache intermediate outputs"
        if isinstance(inputs, (tuple, list)):
            assert len(inputs) <= 10, "Too many inputs."
            input_ids = inputs[0]
            attention_mask = inputs[1] if len(inputs) > 1 else attention_mask
            decoder_input_ids = inputs[2] if len(inputs) > 2 else decoder_input_ids
            decoder_attention_mask = inputs[3] if len(inputs) > 3 else decoder_attention_mask
            encoder_outputs = inputs[4] if len(inputs) > 4 else encoder_outputs
            past_key_values = inputs[5] if len(inputs) > 5 else past_key_values
            use_cache = inputs[6] if len(inputs) > 6 else use_cache
            output_attentions = inputs[7] if len(inputs) > 7 else output_attentions
            output_hidden_states = inputs[8] if len(inputs) > 8 else output_hidden_states
            return_dict = inputs[9] if len(inputs) > 9 else return_dict
        elif isinstance(inputs, (dict, BatchEncoding)):
            assert len(inputs) <= 10, "Too many inputs."
            if "inputs" in inputs:
                raise ValueError("Using `inputs` as a keyword argument is deprecated. Please use `input_ids` instead.")
            input_ids = inputs.get("input_ids")
            attention_mask = inputs.get("attention_mask", attention_mask)
            decoder_input_ids = inputs.get("decoder_input_ids", decoder_input_ids)
            decoder_attention_mask = inputs.get("decoder_attention_mask", decoder_attention_mask)
            encoder_outputs = inputs.get("encoder_outputs", encoder_outputs)
            past_key_values = inputs.get("past_key_values", past_key_values)
            use_cache = inputs.get("use_cache", use_cache)
            output_attentions = inputs.get("output_attentions", output_attentions)
            output_hidden_states = inputs.get("output_hidden_states", output_hidden_states)
        else:
            input_ids = inputs

        use_cache = use_cache if use_cache is not None else self.config.use_cache
        if decoder_input_ids is None:  # Classification
            use_cache = False
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        if not use_cache:
            decoder_input_ids, decoder_padding_mask, causal_mask = self._prepare_bart_decoder_inputs(
                inputs,
                decoder_input_ids=decoder_input_ids,
                decoder_attn_mask=decoder_attention_mask,
                mask_dtype=self.shared.dtype,
            )
        else:
            decoder_padding_mask, causal_mask = None, None
        assert (
            isinstance(encoder_outputs, TFBaseModelOutput) or encoder_outputs is None
        ), f"got unexpected encoder outputs type {type(encoder_outputs)}"
        if encoder_outputs is None:
            encoder_outputs = self.encoder(
                input_ids=input_ids,
                attention_mask=attention_mask,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
                return_dict=True,
                training=training,
            )
        decoder_outputs = self.decoder(
            decoder_input_ids,
            encoder_outputs.last_hidden_state,
            attention_mask,
            decoder_padding_mask,
            decoder_causal_mask=causal_mask,
            decoder_cached_states=past_key_values,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
            training=training,
        )
        if not return_dict:
            # Attention and hidden_states will be [] or None if they aren't needed
            return tuple(x for x in decoder_outputs + encoder_outputs.to_tuple() if x is not None)
        else:
            return TFSeq2SeqModelOutput(
                last_hidden_state=decoder_outputs.last_hidden_state,
                past_key_values=decoder_outputs.past_key_values,
                decoder_hidden_states=decoder_outputs.hidden_states,
                decoder_attentions=decoder_outputs.attentions,
                encoder_last_hidden_state=encoder_outputs.last_hidden_state,
                encoder_hidden_states=encoder_outputs.hidden_states,
                encoder_attentions=encoder_outputs.attentions,
            )
