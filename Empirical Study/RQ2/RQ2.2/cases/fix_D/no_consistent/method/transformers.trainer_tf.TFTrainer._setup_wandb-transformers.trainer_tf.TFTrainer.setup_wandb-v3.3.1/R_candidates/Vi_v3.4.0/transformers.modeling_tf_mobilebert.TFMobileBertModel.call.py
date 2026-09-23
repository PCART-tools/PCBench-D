    @add_start_docstrings_to_callable(MOBILEBERT_INPUTS_DOCSTRING.format("batch_size, sequence_length"))
    @add_code_sample_docstrings(
        tokenizer_class=_TOKENIZER_FOR_DOC,
        checkpoint="google/mobilebert-uncased",
        output_type=TFBaseModelOutputWithPooling,
        config_class=_CONFIG_FOR_DOC,
    )
    def call(self, inputs, **kwargs):
        outputs = self.mobilebert(inputs, **kwargs)
        return outputs
