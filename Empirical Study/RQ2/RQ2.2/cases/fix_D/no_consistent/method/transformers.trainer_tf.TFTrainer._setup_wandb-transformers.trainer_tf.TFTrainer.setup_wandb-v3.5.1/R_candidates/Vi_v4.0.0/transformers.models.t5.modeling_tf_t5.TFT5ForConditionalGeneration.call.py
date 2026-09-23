    @add_start_docstrings_to_model_forward(T5_INPUTS_DOCSTRING)
    @replace_return_docstrings(output_type=TFSeq2SeqLMOutput, config_class=_CONFIG_FOR_DOC)
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
        labels=None,
        use_cache=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
        training=False,
        **kwargs,
    ):
        r"""
        labels (:obj:`tf.Tensor` of shape :obj:`(batch_size, sequence_length)`, `optional`):
            Labels for computing the cross entropy classification loss. Indices should be in ``[0, ...,
            config.vocab_size - 1]``.

        Returns:

        Examples::

            >>> from transformers import T5Tokenizer, TFT5ForConditionalGeneration

            >>> tokenizer = T5Tokenizer.from_pretrained('t5-small')
            >>> model = TFT5ForConditionalGeneration.from_pretrained('t5-small')

            >>> inputs = tokenizer('The <extra_id_0> walks in <extra_id_1> park', return_tensors='tf').input_ids
            >>> labels = tokenizer('<extra_id_0> cute dog <extra_id_1> the <extra_id_2> </s>', return_tensors='tf').input_ids
            >>> outputs = model(inputs, labels=labels)
            >>> loss = outputs.loss
            >>> logits = outputs.logits

            >>> inputs = tokenizer("summarize: studies have shown that owning a dog is good for you ", return_tensors="tf").input_ids  # Batch size 1

            >>> result = model.generate(inputs)

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
            labels = inputs[9] if len(inputs) > 9 else labels
            use_cache = inputs[10] if len(inputs) > 10 else use_cache
            output_attentions = inputs[11] if len(inputs) > 11 else output_attentions
            output_hidden_states = inputs[12] if len(inputs) > 12 else output_hidden_states
            return_dict = inputs[13] if len(inputs) > 13 else return_dict
            assert len(inputs) <= 14, "Too many inputs."
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
            labels = inputs.get("labels", labels)
            use_cache = inputs.get("use_cache", use_cache)
            output_attentions = inputs.get("output_attentions", output_attentions)
            output_hidden_states = inputs.get("output_hidden_states", output_hidden_states)
            return_dict = inputs.get("return_dict", return_dict)
            assert len(inputs) <= 14, "Too many inputs."
        else:
            input_ids = inputs

        use_cache = use_cache if use_cache is not None else self.config.use_cache
        output_attentions = output_attentions if output_attentions else self.config.output_attentions
        output_hidden_states = output_hidden_states if output_hidden_states else self.config.output_hidden_states
        return_dict = return_dict if return_dict is not None else self.config.return_dict

        # Encode if needed (training, first prediction pass)
        if encoder_outputs is None:
            encoder_outputs = self.encoder(
                input_ids,
                attention_mask=attention_mask,
                inputs_embeds=inputs_embeds,
                head_mask=head_mask,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
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

        sequence_output = decoder_outputs[0]

        # T5v1.1 does not tie output word embeddings and thus does not require downscaling
        if self.config.tie_word_embeddings:
            sequence_output = sequence_output * (self.model_dim ** -0.5)
            logits = self.get_output_embeddings()(sequence_output, mode="linear")
        else:
            logits = self.get_output_embeddings()(sequence_output)

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
