    @add_start_docstrings_to_callable(T5_INPUTS_DOCSTRING)
    @replace_return_docstrings(output_type=TFSeq2SeqLMOutput, config_class=_CONFIG_FOR_DOC)
    def call(
        self,
        inputs,
        attention_mask=None,
        encoder_outputs=None,
        inputs_embeds=None,
        head_mask=None,
        past_key_values=None,
        decoder_input_ids=None,
        decoder_attention_mask=None,
        decoder_inputs_embeds=None,
        use_cache=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
        labels=None,
        training=False,
        **kwargs,
    ):
        r"""
        labels (:obj:`tf.Tensor` of shape :obj:`(batch_size, sequence_length)`, `optional`):
            Labels for computing the cross entropy classification loss.
            Indices should be in ``[0, ..., config.vocab_size - 1]``.

        Returns:

        Examples::

            >>> from transformers import T5Tokenizer, TFT5ForConditionalGeneration

            >>> tokenizer = T5Tokenizer.from_pretrained('t5-small')
            >>> model = TFT5ForConditionalGeneration.from_pretrained('t5-small')
            >>> inputs = tokenizer.encode("Hello, my dog is cute", return_tensors="tf")  # Batch size 1
            >>> outputs = model(inputs, decoder_input_ids=inputs)
            >>> prediction_scores = outputs[0]

            >>> tokenizer = T5Tokenizer.from_pretrained('t5-small')
            >>> model = TFT5ForConditionalGeneration.from_pretrained('t5-small')
            >>> inputs = tokenizer.encode("summarize: Hello, my dog is cute", return_tensors="tf")  # Batch size 1
            >>> result = model.generate(inputs)

        """
        if isinstance(inputs, (tuple, list)):
            input_ids = inputs[0]
            attention_mask = inputs[1] if len(inputs) > 1 else attention_mask
            encoder_outputs = inputs[2] if len(inputs) > 2 else encoder_outputs
            inputs_embeds = inputs[3] if len(inputs) > 3 else inputs_embeds
            head_mask = inputs[4] if len(inputs) > 4 else head_mask
            past_key_values = inputs[5] if len(inputs) > 5 else past_key_values
            decoder_input_ids = inputs[6] if len(inputs) > 6 else decoder_input_ids
            decoder_attention_mask = inputs[7] if len(inputs) > 7 else decoder_attention_mask
            decoder_inputs_embeds = inputs[8] if len(inputs) > 8 else decoder_inputs_embeds
            use_cache = inputs[9] if len(inputs) > 9 else use_cache
            output_attentions = inputs[10] if len(inputs) > 10 else output_attentions
            output_hidden_states = inputs[11] if len(inputs) > 11 else output_hidden_states
            return_dict = inputs[12] if len(inputs) > 12 else return_dict
            labels = inputs[13] if len(inputs) > 13 else labels
            assert len(inputs) <= 14, "Too many inputs."
        elif isinstance(inputs, (dict, BatchEncoding)):
            if "inputs" in inputs:
                warnings.warn("Using `inputs` as a keyword argument is deprecated. Please use `input_ids` instead.")
                input_ids = inputs.get("inputs")
            input_ids = inputs.get("input_ids")
            attention_mask = inputs.get("attention_mask", attention_mask)
            encoder_outputs = inputs.get("encoder_outputs", encoder_outputs)
            inputs_embeds = inputs.get("inputs_embeds", inputs_embeds)
            head_mask = inputs.get("head_mask", head_mask)
            past_key_values = inputs.get("past_key_values", past_key_values)
            decoder_input_ids = inputs.get("decoder_input_ids", decoder_input_ids)
            decoder_attention_mask = inputs.get("decoder_attention_mask", decoder_attention_mask)
            decoder_inputs_embeds = inputs.get("decoder_inputs_embeds", decoder_inputs_embeds)
            use_cache = inputs.get("use_cache", use_cache)
            output_attentions = inputs.get("output_attentions", output_attentions)
            output_hidden_states = inputs.get("output_hidden_states", output_hidden_states)
            return_dict = inputs.get("return_dict", return_dict)
            labels = inputs.get("labels", labels)
            assert len(inputs) <= 14, "Too many inputs."

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
        return_dict = return_dict if return_dict is not None else self.config.return_dict

        # Encode if needed (training, first prediction pass)
        if encoder_outputs is None:
            # Convert encoder inputs in embeddings if needed
            encoder_outputs = self.encoder(
                [
                    input_ids,
                    attention_mask,
                    None,
                    None,
                    inputs_embeds,
                    head_mask,
                    None,
                    False,
                    output_attentions,
                    output_hidden_states,
                ],
                training=training,
            )

        hidden_states = encoder_outputs[0]

        if labels is not None and decoder_input_ids is None and decoder_inputs_embeds is None:
            # get decoder inputs from shifting lm labels to the right
            decoder_input_ids = self._shift_right(labels)

        # If decoding with past key value states, only the last tokens
        # should be given as an input
        if past_key_values is not None:
            if decoder_input_ids is not None:
                decoder_input_ids = decoder_input_ids[:, -1:]
            if decoder_inputs_embeds is not None:
                decoder_inputs_embeds = decoder_inputs_embeds[:, -1:]

        # Decode
        decoder_outputs = self.decoder(
            [
                decoder_input_ids,
                decoder_attention_mask,
                hidden_states,
                attention_mask,
                decoder_inputs_embeds,
                head_mask,
                past_key_values,
                use_cache,
                output_attentions,
                output_hidden_states,
            ],
            training=training,
        )

        sequence_output = decoder_outputs[0] * (self.model_dim ** -0.5)
        embed_tokens = self.get_output_embeddings()
        logits = embed_tokens(sequence_output, mode="linear")

        loss = None if labels is None else self.compute_loss(labels, logits)

        past = (
            (encoder_outputs, decoder_outputs[1]) if cast_bool_to_primitive(use_cache, self.config.use_cache) else None
        )
        if not return_dict:
            if past is not None:
                decoder_outputs = decoder_outputs[:1] + (past,) + decoder_outputs[2:]
            output = (logits,) + decoder_outputs[1:] + encoder_outputs
            return ((loss,) + output) if loss is not None else output

        # Putting this before breaks tf compilation.
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )

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

        return TFSeq2SeqLMOutput(
            loss=loss,
            logits=logits,
            past_key_values=past,
            decoder_hidden_states=decoder_outputs[2],
            decoder_attentions=decoder_outputs[3],
            encoder_last_hidden_state=encoder_outputs[0],
            encoder_hidden_states=encoder_outputs[1],
            encoder_attentions=encoder_outputs[2],
        )
