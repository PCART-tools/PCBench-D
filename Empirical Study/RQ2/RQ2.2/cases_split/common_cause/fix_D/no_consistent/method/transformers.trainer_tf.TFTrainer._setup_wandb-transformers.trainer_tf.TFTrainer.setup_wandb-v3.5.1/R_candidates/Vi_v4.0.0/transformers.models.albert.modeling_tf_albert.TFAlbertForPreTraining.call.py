    @add_start_docstrings_to_model_forward(ALBERT_INPUTS_DOCSTRING.format("batch_size, sequence_length"))
    @replace_return_docstrings(output_type=TFAlbertForPreTrainingOutput, config_class=_CONFIG_FOR_DOC)
    def call(self, inputs, **kwargs):
        r"""
        Return:

        Example::

            >>> import tensorflow as tf
            >>> from transformers import AlbertTokenizer, TFAlbertForPreTraining

            >>> tokenizer = AlbertTokenizer.from_pretrained('albert-base-v2')
            >>> model = TFAlbertForPreTraining.from_pretrained('albert-base-v2')

            >>> input_ids = tf.constant(tokenizer.encode("Hello, my dog is cute", add_special_tokens=True))[None, :]  # Batch size 1
            >>> outputs = model(input_ids)

            >>> prediction_logits = outputs.prediction_logits
            >>> sop_logits = outputs.sop_logits
        """
        return_dict = kwargs.get("return_dict")
        return_dict = return_dict if return_dict is not None else self.albert.return_dict
        outputs = self.albert(inputs, **kwargs)
        sequence_output, pooled_output = outputs[:2]
        prediction_scores = self.predictions(sequence_output)
        sop_scores = self.sop_classifier(pooled_output, training=kwargs.get("training", False))

        if not return_dict:
            return (prediction_scores, sop_scores) + outputs[2:]

        return TFAlbertForPreTrainingOutput(
            prediction_logits=prediction_scores,
            sop_logits=sop_scores,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )
