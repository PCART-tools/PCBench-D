    @add_start_docstrings_to_callable(OPENAI_GPT_INPUTS_DOCSTRING)
    @replace_return_docstrings(output_type=TFOpenAIGPTDoubleHeadsModelOutput, config_class=_CONFIG_FOR_DOC)
    def call(
        self,
        inputs,
        attention_mask=None,
        token_type_ids=None,
        position_ids=None,
        head_mask=None,
        inputs_embeds=None,
        mc_token_ids=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
        training=False,
    ):
        r"""
        mc_token_ids (:obj:`tf.Tensor` or :obj:`Numpy array` of shape :obj:`(batch_size, num_choices)`, `optional`, default to index of the last token of the input)
            Index of the classification token in each input sequence.
            Selected in the range ``[0, input_ids.size(-1) - 1]``.

        Return:

        Examples::

            >>> import tensorflow as tf
            >>> from transformers import OpenAIGPTTokenizer, TFOpenAIGPTDoubleHeadsModel

            >>> tokenizer = OpenAIGPTTokenizer.from_pretrained('openai-gpt')
            >>> model = TFOpenAIGPTDoubleHeadsModel.from_pretrained('openai-gpt')

            >>> # Add a [CLS] to the vocabulary (we should train it also!)
            >>> tokenizer.add_special_tokens({'cls_token': '[CLS]'})
            >>> model.resize_token_embeddings(len(tokenizer))  # Update the model embeddings with the new vocabulary size
            >>> print(tokenizer.cls_token_id, len(tokenizer))  # The newly token the last token of the vocabulary

            >>> choices = ["Hello, my dog is cute [CLS]", "Hello, my cat is cute [CLS]"]
            >>> encoding = tokenizer(choices, return_tensors="tf")
            >>> inputs = {k: tf.expand_dims(v, 0) for k, v in encoding.items()}
            >>> inputs["mc_token_ids"]= tf.constant([inputs["input_ids"].shape[-1] - 1, inputs["input_ids"].shape[-1] - 1])[None, :]  # Batch size 1
            >>> outputs = model(inputs)
            >>> lm_prediction_scores, mc_prediction_scores = outputs[:2]
        """

        if isinstance(inputs, (tuple, list)):
            input_ids = inputs[0]
            attention_mask = inputs[1] if len(inputs) > 1 else attention_mask
            token_type_ids = inputs[2] if len(inputs) > 2 else token_type_ids
            position_ids = inputs[3] if len(inputs) > 3 else position_ids
            head_mask = inputs[4] if len(inputs) > 4 else head_mask
            inputs_embeds = inputs[5] if len(inputs) > 5 else inputs_embeds
            mc_token_ids = inputs[6] if len(inputs) > 6 else mc_token_ids
            output_attentions = inputs[7] if len(inputs) > 7 else output_attentions
            output_hidden_states = inputs[8] if len(inputs) > 8 else output_hidden_states
            return_dict = inputs[9] if len(inputs) > 9 else return_dict
            assert len(inputs) <= 10, "Too many inputs."
        elif isinstance(inputs, (dict, BatchEncoding)):
            input_ids = inputs.get("input_ids")
            attention_mask = inputs.get("attention_mask", attention_mask)
            token_type_ids = inputs.get("token_type_ids", token_type_ids)
            position_ids = inputs.get("position_ids", position_ids)
            head_mask = inputs.get("head_mask", head_mask)
            inputs_embeds = inputs.get("inputs_embeds", inputs_embeds)
            mc_token_ids = inputs.get("mc_token_ids", mc_token_ids)
            output_attentions = inputs.get("output_attentions", output_attentions)
            output_hidden_states = inputs.get("output_hidden_states", output_hidden_states)
            return_dict = inputs.get("return_dict", return_dict)
            assert len(inputs) <= 10, "Too many inputs."
        else:
            input_ids = inputs
        return_dict = return_dict if return_dict is not None else self.transformer.return_dict

        if input_ids is not None:
            input_shapes = shape_list(input_ids)
        else:
            input_shapes = shape_list(inputs_embeds)[:-1]

        seq_length = input_shapes[-1]
        flat_input_ids = tf.reshape(input_ids, (-1, seq_length)) if input_ids is not None else None
        flat_attention_mask = tf.reshape(attention_mask, (-1, seq_length)) if attention_mask is not None else None
        flat_token_type_ids = tf.reshape(token_type_ids, (-1, seq_length)) if token_type_ids is not None else None
        flat_position_ids = tf.reshape(position_ids, (-1, seq_length)) if position_ids is not None else None
        transformer_outputs = self.transformer(
            flat_input_ids,
            flat_attention_mask,
            flat_token_type_ids,
            flat_position_ids,
            head_mask,
            inputs_embeds,
            output_attentions,
            output_hidden_states,
            return_dict=return_dict,
            training=training,
        )
        hidden_states = transformer_outputs[0]
        hidden_states = tf.reshape(hidden_states, input_shapes + shape_list(hidden_states)[-1:])
        lm_logits = self.transformer.tokens_embed(hidden_states, mode="linear")
        mc_logits = self.multiple_choice_head(hidden_states, mc_token_ids, training=training)
        mc_logits = tf.squeeze(mc_logits, axis=-1)

        if not return_dict:
            return (lm_logits, mc_logits) + transformer_outputs[1:]

        return TFOpenAIGPTDoubleHeadsModelOutput(
            logits=lm_logits,
            mc_logits=mc_logits,
            hidden_states=transformer_outputs.hidden_states,
            attentions=transformer_outputs.attentions,
        )
