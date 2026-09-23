    @add_start_docstrings_to_model_forward(LONGFORMER_INPUTS_DOCSTRING.format("batch_size, sequence_length"))
    @add_code_sample_docstrings(
        tokenizer_class=_TOKENIZER_FOR_DOC,
        checkpoint="allenai/longformer-large-4096-finetuned-triviaqa",
        output_type=TFLongformerQuestionAnsweringModelOutput,
        config_class=_CONFIG_FOR_DOC,
    )
    def call(
        self,
        inputs=None,
        attention_mask=None,
        global_attention_mask=None,
        token_type_ids=None,
        position_ids=None,
        inputs_embeds=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
        start_positions=None,
        end_positions=None,
        training=False,
    ):
        r"""
        start_positions (:obj:`tf.Tensor` of shape :obj:`(batch_size,)`, `optional`):
            Labels for position (index) of the start of the labelled span for computing the token classification loss.
            Positions are clamped to the length of the sequence (`sequence_length`). Position outside of the sequence
            are not taken into account for computing the loss.
        end_positions (:obj:`tf.Tensor` of shape :obj:`(batch_size,)`, `optional`):
            Labels for position (index) of the end of the labelled span for computing the token classification loss.
            Positions are clamped to the length of the sequence (`sequence_length`). Position outside of the sequence
            are not taken into account for computing the loss.
        """
        return_dict = return_dict if return_dict is not None else self.longformer.return_dict

        if isinstance(inputs, (tuple, list)):
            input_ids = inputs[0]
            global_attention_mask = inputs[2]
            start_positions = inputs[9] if len(inputs) > 9 else start_positions
            end_positions = inputs[10] if len(inputs) > 10 else end_positions
            if len(inputs) > 9:
                inputs = inputs[:9]
        elif isinstance(inputs, (dict, BatchEncoding)):
            input_ids = inputs.get("input_ids", inputs)
            global_attention_mask = inputs.get("global_attention_mask", global_attention_mask)
            start_positions = inputs.pop("start_positions", start_positions)
            end_positions = inputs.pop("end_positions", start_positions)
        else:
            input_ids = inputs

        # set global attention on question tokens
        if global_attention_mask is None and input_ids is not None:
            if input_ids is None:
                logger.warning(
                    "It is not possible to automatically generate the `global_attention_mask`. Please make sure that it is correctly set."
                )
            elif tf.where(input_ids == self.config.sep_token_id).shape[0] != 3 * input_ids.shape[0]:
                logger.warning(
                    f"There should be exactly three separator tokens: {self.config.sep_token_id} in every sample for questions answering. You might also consider to set `global_attention_mask` manually in the forward function to avoid this. This is most likely an error."
                )
            else:
                logger.info("Initializing global attention on question tokens...")
                # put global attention on all tokens until `config.sep_token_id` is reached
                sep_token_indices = tf.where(input_ids == self.config.sep_token_id)
                global_attention_mask = _compute_global_attention_mask(shape_list(input_ids), sep_token_indices)

        outputs = self.longformer(
            inputs,
            attention_mask=attention_mask,
            global_attention_mask=global_attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            inputs_embeds=inputs_embeds,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
            training=training,
        )
        sequence_output = outputs[0]
        logits = self.qa_outputs(sequence_output)
        start_logits, end_logits = tf.split(logits, 2, axis=-1)
        start_logits = tf.squeeze(start_logits, axis=-1)
        end_logits = tf.squeeze(end_logits, axis=-1)
        loss = None

        if start_positions is not None and end_positions is not None:
            labels = {"start_position": start_positions}
            labels["end_position"] = end_positions
            loss = self.compute_loss(labels, (start_logits, end_logits))

        if not return_dict:
            output = (start_logits, end_logits) + outputs[2:]

            return ((loss,) + output) if loss is not None else output

        return TFLongformerQuestionAnsweringModelOutput(
            loss=loss,
            start_logits=start_logits,
            end_logits=end_logits,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
            global_attentions=outputs.global_attentions,
        )
