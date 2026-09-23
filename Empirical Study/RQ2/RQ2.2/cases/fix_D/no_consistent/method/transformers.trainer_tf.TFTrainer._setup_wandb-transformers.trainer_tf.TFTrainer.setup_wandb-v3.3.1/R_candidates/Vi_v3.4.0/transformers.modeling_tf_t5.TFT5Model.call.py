    @add_start_docstrings_to_callable(T5_INPUTS_DOCSTRING)
    @replace_return_docstrings(output_type=TFSeq2SeqModelOutput, config_class=_CONFIG_FOR_DOC)
    def call(
        self,
        inputs,
        attention_mask=None,
        decoder_input_ids=None,
        decoder_attention_mask=None,
        encoder_outputs=None,
        past_key_values=None,
        head_mask=None,
        inputs_embeds=None,
        decoder_inputs_embeds=None,
        use_cache=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
        training=False,
        **kwargs,
    ):
        r"""
        Returns:

        Examples::

            >>> from transformers import T5Tokenizer, TFT5Model

            >>> tokenizer = T5Tokenizer.from_pretrained('t5-small')
            >>> model = TFT5Model.from_pretrained('t5-small')

            >>> input_ids = tokenizer("Studies have been shown that owning a dog is good for you", return_tensors="tf").input_ids  # Batch size 1
            >>> decoder_input_ids = tokenizer("Studies show that", return_tensors="tf").input_ids  # Batch size 1
            >>> outputs = model(input_ids, decoder_input_ids=decoder_input_ids, return_dict=True)


        """
        if isinstance(inputs, (tuple, list)):
            input_ids = inputs[0]
            attention_mask = inputs[1] if len(inputs) > 1 else attention_mask
            decoder_input_ids = inputs[2] if len(inputs) > 2 else decoder_input_ids
            decoder_attention_mask = inputs[3] if len(inputs) > 3 else decoder_attention_mask
            encoder_outputs = inputs[4] if len(inputs) > 4 else encoder_outputs
            past_key_values = inputs[5] if len(inputs) > 5 else head_mask
            head_mask = inputs[6] if len(inputs) > 6 else head_mask
            inputs_embeds = inputs[7] if len(inputs) > 7 else inputs_embeds
            decoder_inputs_embeds = inputs[8] if len(inputs) > 8 else decoder_inputs_embeds
            use_cache = inputs[9] if len(inputs) > 9 else use_cache
            output_attentions = inputs[10] if len(inputs) > 10 else output_attentions
            output_hidden_states = inputs[11] if len(inputs) > 11 else output_hidden_states
            return_dict = inputs[12] if len(inputs) > 12 else return_dict
            assert len(inputs) <= 13, "Too many inputs."
        elif isinstance(inputs, (dict, BatchEncoding)):
            if "inputs" in inputs:
                warnings.warn("Using `inputs` as a keyword argument is deprecated. Please use `input_ids` instead.")
                input_ids = inputs.get("inputs")
            input_ids = inputs.get("input_ids")
            attention_mask = inputs.get("attention_mask", attention_mask)
            decoder_input_ids = inputs.get("decoder_input_ids", decoder_input_ids)
            decoder_attention_mask = inputs.get("decoder_attention_mask", decoder_attention_mask)
            encoder_outputs = inputs.get("encoder_outputs", encoder_outputs)
            past_key_values = inputs.get("past_key_values", past_key_values)
            head_mask = inputs.get("head_mask", head_mask)
            inputs_embeds = inputs.get("inputs_embeds", inputs_embeds)
            decoder_inputs_embeds = inputs.get("decoder_inputs_embeds", decoder_inputs_embeds)
            use_cache = inputs.get("use_cache", use_cache)
            output_attentions = inputs.get("output_attentions", output_attentions)
            output_hidden_states = inputs.get("output_hidden_states", output_hidden_states)
            assert len(inputs) <= 13, "Too many inputs."

            if "past_key_value_states" in inputs:
                warnings.warn(
                    "The `past_key_value_states` argument is deprecated and will be removed in a future version, use `past_key_values` instead.",
                    FutureWarning,
                )
                past_key_values = inputs.pop("past_key_value_states")
        else:
            input_ids = inputs

            if "past_key_value_states" in kwargs:
                warnings.warn(
                    "The `past_key_value_states` argument is deprecated and will be removed in a future version, use `past_key_values` instead.",
                    FutureWarning,
                )
                past_key_values = kwargs.pop("past_key_value_states")

        use_cache = use_cache if use_cache is not None else self.config.use_cache
        output_attentions = output_attentions if output_attentions else self.config.output_attentions
        output_hidden_states = output_hidden_states if output_hidden_states else self.config.output_hidden_states
        return_dict = return_dict if return_dict is not None else self.config.return_dict

        # Encode if needed (training, first prediction pass)
        if encoder_outputs is None:
            encoder_outputs = self.encoder(
                input_ids,
                attention_mask=attention_mask,
                encoder_hidden_states=None,
                encoder_attention_mask=None,
                inputs_embeds=inputs_embeds,
                head_mask=head_mask,
                past_key_values=None,
                use_cache=False,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
                training=training,
            )

        hidden_states = encoder_outputs[0]

        # Decode
        decoder_outputs = self.decoder(
            decoder_input_ids,
            attention_mask=decoder_attention_mask,
            encoder_hidden_states=hidden_states,
            encoder_attention_mask=attention_mask,
            inputs_embeds=decoder_inputs_embeds,
            head_mask=head_mask,
            past_key_values=past_key_values,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            training=training,
        )

        past = (
            (encoder_outputs, decoder_outputs[1]) if cast_bool_to_primitive(use_cache, self.config.use_cache) else None
        )
        if not return_dict:
            if past is not None:
                decoder_outputs = decoder_outputs[:1] + (past,) + decoder_outputs[2:]
            return decoder_outputs + encoder_outputs

        # This is long and annoying but if we introduce return_dict at the TFT5MainLayer level (like in PyTorch)
        # TF refuses to compile anymore.
        if not cast_bool_to_primitive(use_cache, self.config.use_cache):
            decoder_outputs = decoder_outputs[:1] + (None,) + decoder_outputs[1:]
        if not cast_bool_to_primitive(output_hidden_states, self.config.output_hidden_states):
            encoder_outputs = encoder_outputs[:1] + (None,) + encoder_outputs[1:]
            decoder_outputs = decoder_outputs[:2] + (None,) + decoder_outputs[2:]
        if not cast_bool_to_primitive(output_attentions, self.config.output_attentions):
            encoder_outputs = encoder_outputs + (None,)
            decoder_outputs = decoder_outputs + (None,)

        return TFSeq2SeqModelOutput(
            last_hidden_state=decoder_outputs[0],
            past_key_values=past,
            decoder_hidden_states=decoder_outputs[2],
            decoder_attentions=decoder_outputs[3],
            encoder_last_hidden_state=encoder_outputs[0],
            encoder_hidden_states=encoder_outputs[1],
            encoder_attentions=encoder_outputs[2],
        )
