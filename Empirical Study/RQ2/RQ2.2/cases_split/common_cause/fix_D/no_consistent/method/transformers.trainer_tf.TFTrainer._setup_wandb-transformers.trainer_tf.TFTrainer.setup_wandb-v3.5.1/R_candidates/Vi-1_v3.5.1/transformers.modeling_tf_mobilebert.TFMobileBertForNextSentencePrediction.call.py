    @add_start_docstrings_to_model_forward(MOBILEBERT_INPUTS_DOCSTRING.format("batch_size, sequence_length"))
    @replace_return_docstrings(output_type=TFNextSentencePredictorOutput, config_class=_CONFIG_FOR_DOC)
    def call(self, inputs, **kwargs):
        r"""
        Return:

        Examples::

            >>> import tensorflow as tf
            >>> from transformers import MobileBertTokenizer, TFMobileBertForNextSentencePrediction

            >>> tokenizer = MobileBertTokenizer.from_pretrained('google/mobilebert-uncased')
            >>> model = TFMobileBertForNextSentencePrediction.from_pretrained('google/mobilebert-uncased')

            >>> prompt = "In Italy, pizza served in formal settings, such as at a restaurant, is presented unsliced."
            >>> next_sentence = "The sky is blue due to the shorter wavelength of blue light."
            >>> encoding = tokenizer(prompt, next_sentence, return_tensors='tf')

            >>> logits = model(encoding['input_ids'], token_type_ids=encoding['token_type_ids'])[0]
        """
        return_dict = kwargs.get("return_dict")
        return_dict = return_dict if return_dict is not None else self.mobilebert.return_dict
        outputs = self.mobilebert(inputs, **kwargs)

        pooled_output = outputs[1]
        seq_relationship_score = self.cls(pooled_output)

        if not return_dict:
            return (seq_relationship_score,) + outputs[2:]

        return TFNextSentencePredictorOutput(
            logits=seq_relationship_score,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )
