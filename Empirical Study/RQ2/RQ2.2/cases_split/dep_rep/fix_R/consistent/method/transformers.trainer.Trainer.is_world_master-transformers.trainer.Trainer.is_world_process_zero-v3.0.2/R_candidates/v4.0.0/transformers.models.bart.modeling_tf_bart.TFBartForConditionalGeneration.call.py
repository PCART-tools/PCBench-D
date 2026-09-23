    @add_start_docstrings_to_model_forward(BART_INPUTS_DOCSTRING)
    @replace_return_docstrings(output_type=TFSeq2SeqLMOutput, config_class=_CONFIG_FOR_DOC)
    def call(
        self,
        inputs,
        attention_mask=None,
        decoder_input_ids=None,
        decoder_attention_mask=None,
        encoder_outputs: Optional[TFBaseModelOutput] = None,
        past_key_values=None,
        labels=None,
        use_cache=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
        training=False,
        **kwargs,
    ):
        """
        Returns:

        Examples::

            # Mask filling only works for bart-large
            from transformers import BartTokenizer, TFBartForConditionalGeneration
            import tensorflow as tf
            mname = 'facebook/bart-large'
            tokenizer = BartTokenizer.from_pretrained(mname)
            TXT = "My friends are <mask> but they eat too many carbs."
            model = TFBartForConditionalGeneration.from_pretrained(mname)
            batch = tokenizer([TXT], return_tensors='tf')
            logits = model(inputs=batch.input_ids).logits
            probs = tf.nn.softmax(logits[0])
            # probs[5] is associated with the mask token
        """
        if isinstance(inputs, (tuple, list)):
            input_ids = inputs[0]
            attention_mask = inputs[1] if len(inputs) > 1 else attention_mask
            decoder_input_ids = inputs[2] if len(inputs) > 2 else decoder_input_ids
            decoder_attention_mask = inputs[3] if len(inputs) > 3 else decoder_attention_mask
            encoder_outputs = inputs[4] if len(inputs) > 4 else encoder_outputs
            past_key_values = inputs[5] if len(inputs) > 5 else past_key_values
            labels = inputs[6] if len(inputs) > 6 else labels
            use_cache = inputs[7] if len(inputs) > 7 else use_cache
            output_attentions = inputs[8] if len(inputs) > 8 else output_attentions
            output_hidden_states = inputs[9] if len(inputs) > 9 else output_hidden_states
            return_dict = inputs[10] if len(inputs) > 10 else return_dict
            assert len(inputs) <= 13, "Too many inputs."
        elif isinstance(inputs, (dict, BatchEncoding)):
            if "inputs" in inputs:
                warnings.warn("Using `inputs` as a keyword argument is deprecated. Please use `input_ids` instead.")
            if "past_key_value_states" in inputs:
                raise ValueError(PAST_KV_DEPRECATION_WARNING)
            input_ids = inputs.get("input_ids")
            attention_mask = inputs.get("attention_mask", attention_mask)
            decoder_input_ids = inputs.get("decoder_input_ids", decoder_input_ids)
            decoder_attention_mask = inputs.get("decoder_attention_mask", decoder_attention_mask)
            encoder_outputs = inputs.get("encoder_outputs", encoder_outputs)
            past_key_values = inputs.get("past_key_values", past_key_values)
            labels = inputs.get("labels", labels)
            use_cache = inputs.get("use_cache", use_cache)
            output_attentions = inputs.get("output_attentions", output_attentions)
            output_hidden_states = inputs.get("output_hidden_states", output_hidden_states)
            assert len(inputs) <= 13, "Too many inputs."

        else:
            input_ids = inputs
        if "past_key_value_states" in kwargs:
            raise ValueError(PAST_KV_DEPRECATION_WARNING)

        output_attentions = output_attentions if output_attentions else self.config.output_attentions
        output_hidden_states = output_hidden_states if output_hidden_states else self.config.output_hidden_states
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict
        use_cache = use_cache if use_cache is not None else self.config.use_cache
        if labels is not None:
            use_cache = False
        outputs: TFSeq2SeqModelOutput = self.model(
            input_ids,
            attention_mask=attention_mask,
            decoder_input_ids=decoder_input_ids,
            encoder_outputs=encoder_outputs,
            decoder_attention_mask=decoder_attention_mask,
            past_key_values=past_key_values,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=True,  # TODO(SS): this may need to change to support compilation
        )
        logits = self.model.shared(outputs.last_hidden_state, mode="linear")
        logits = logits + self.final_logits_bias
        loss = None if labels is None else self.compute_loss(labels, logits)

        past = outputs.past_key_values if cast_bool_to_primitive(use_cache, self.config.use_cache) else None

        if return_dict:
            return TFSeq2SeqLMOutput(
                loss=loss,
                logits=logits,
                past_key_values=past,  # index 1 of d outputs
                decoder_hidden_states=outputs.decoder_hidden_states,  # index 2 of d outputs
                decoder_attentions=outputs.decoder_attentions,  # index 3 of d outputs
                encoder_last_hidden_state=outputs.last_hidden_state,  # index 0 of encoder outputs
                encoder_hidden_states=outputs.encoder_hidden_states,  # 1 of e out
                encoder_attentions=outputs.encoder_attentions,  # 2 of e out
            )
        else:
            if past is not None:
                decoder_outputs = (past,)
            else:
                decoder_outputs = tuple(
                    [x for x in (outputs.decoder_hidden_states, outputs.decoder_attentions) if x is not None]
                )
            enc_out = (outputs.encoder_last_hidden_state, outputs.encoder_hidden_states, outputs.encoder_attentions)
            encoder_outputs = tuple(x for x in enc_out if x is not None)
            output: Tuple = (logits,) + decoder_outputs + encoder_outputs
            return ((loss,) + output) if loss is not None else output
