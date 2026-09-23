    @add_start_docstrings_to_callable(ELECTRA_INPUTS_DOCSTRING.format("batch_size, sequence_length"))
    @replace_return_docstrings(output_type=TFElectraForPreTrainingOutput, config_class=_CONFIG_FOR_DOC)
    def call(
        self,
        inputs,
        attention_mask=None,
        token_type_ids=None,
        position_ids=None,
        head_mask=None,
        inputs_embeds=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
        training=False,
        **kwargs,
    ):
        r"""
        Returns:

        Examples::

            >>> import tensorflow as tf
            >>> from transformers import ElectraTokenizer, TFElectraForPreTraining

            >>> tokenizer = ElectraTokenizer.from_pretrained('google/electra-small-discriminator')
            >>> model = TFElectraForPreTraining.from_pretrained('google/electra-small-discriminator')
            >>> input_ids = tf.constant(tokenizer.encode("Hello, my dog is cute"))[None, :]  # Batch size 1
            >>> outputs = model(input_ids)
            >>> scores = outputs[0]
        """
        return_dict = return_dict if return_dict is not None else self.electra.config.return_dict

        if inputs is None and "input_ids" in kwargs and isinstance(kwargs["input_ids"], (dict, BatchEncoding)):
            warnings.warn(
                "Using `input_ids` as a dictionary keyword argument is deprecated. Please use `inputs` instead."
            )
            inputs = kwargs["input_ids"]

        discriminator_hidden_states = self.electra(
            inputs,
            attention_mask,
            token_type_ids,
            position_ids,
            head_mask,
            inputs_embeds,
            output_attentions,
            output_hidden_states,
            return_dict=return_dict,
            training=training,
        )
        discriminator_sequence_output = discriminator_hidden_states[0]
        logits = self.discriminator_predictions(discriminator_sequence_output)

        if not return_dict:
            return (logits,) + discriminator_hidden_states[1:]

        return TFElectraForPreTrainingOutput(
            logits=logits,
            hidden_states=discriminator_hidden_states.hidden_states,
            attentions=discriminator_hidden_states.attentions,
        )
