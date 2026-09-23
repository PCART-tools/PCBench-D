    @add_start_docstrings_to_callable(DISTILBERT_INPUTS_DOCSTRING.format("batch_size, sequence_length"))
    @add_code_sample_docstrings(
        tokenizer_class=_TOKENIZER_FOR_DOC,
        checkpoint="distilbert-base-uncased",
        output_type=TFBaseModelOutput,
        config_class=_CONFIG_FOR_DOC,
    )
    def call(self, inputs, **kwargs):
        outputs = self.distilbert(inputs, **kwargs)
        return outputs
