    @add_start_docstrings_to_model_forward(MOBILEBERT_INPUTS_DOCSTRING.format("batch_size, sequence_length"))
    @replace_return_docstrings(output_type=TFMobileBertForPreTrainingOutput, config_class=_CONFIG_FOR_DOC)
    def call(self, inputs, **kwargs):
        r"""
        Return:

        Examples::

            >>> import tensorflow as tf
            >>> from transformers import MobileBertTokenizer, TFMobileBertForPreTraining

            >>> tokenizer = MobileBertTokenizer.from_pretrained('google/mobilebert-uncased')
            >>> model = TFMobileBertForPreTraining.from_pretrained('google/mobilebert-uncased')
            >>> input_ids = tf.constant(tokenizer.encode("Hello, my dog is cute"))[None, :]  # Batch size 1
            >>> outputs = model(input_ids)
            >>> prediction_scores, seq_relationship_scores = outputs[:2]

        """
        return_dict = kwargs.get("return_dict")
        return_dict = return_dict if return_dict is not None else self.mobilebert.return_dict
        outputs = self.mobilebert(inputs, **kwargs)

        sequence_output, pooled_output = outputs[:2]
        prediction_scores = self.predictions(sequence_output)
        seq_relationship_score = self.seq_relationship(pooled_output)

        if not return_dict:
            return (prediction_scores, seq_relationship_score) + outputs[2:]

        return TFMobileBertForPreTrainingOutput(
            prediction_logits=prediction_scores,
            seq_relationship_logits=seq_relationship_score,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )
