    @add_start_docstrings_to_callable(FLAUBERT_INPUTS_DOCSTRING)
    @add_code_sample_docstrings(
        tokenizer_class=_TOKENIZER_FOR_DOC,
        checkpoint="jplu/tf-flaubert-small-cased",
        output_type=TFBaseModelOutput,
        config_class=_CONFIG_FOR_DOC,
    )
    def call(self, inputs, **kwargs):
        outputs = self.transformer(inputs, **kwargs)
        return outputs
