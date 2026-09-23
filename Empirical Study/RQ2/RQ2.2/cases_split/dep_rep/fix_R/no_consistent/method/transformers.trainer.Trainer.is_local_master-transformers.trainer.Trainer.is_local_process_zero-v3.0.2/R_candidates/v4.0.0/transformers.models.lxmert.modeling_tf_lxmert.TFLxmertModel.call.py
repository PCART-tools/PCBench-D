    @add_start_docstrings_to_model_forward(LXMERT_INPUTS_DOCSTRING)
    @add_code_sample_docstrings(
        tokenizer_class=_TOKENIZER_FOR_DOC,
        checkpoint="unc-nlp/lxmert-base-uncased",
        output_type=TFLxmertModelOutput,
        config_class=_CONFIG_FOR_DOC,
    )
    def call(self, inputs, *args, **kwargs):
        outputs = self.lxmert(inputs, *args, **kwargs)
        return outputs
