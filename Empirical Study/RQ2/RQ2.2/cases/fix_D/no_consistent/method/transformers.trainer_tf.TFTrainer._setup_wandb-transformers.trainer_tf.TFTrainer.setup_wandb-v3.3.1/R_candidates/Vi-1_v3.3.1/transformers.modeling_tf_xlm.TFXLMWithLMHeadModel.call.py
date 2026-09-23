    @add_start_docstrings_to_callable(XLM_INPUTS_DOCSTRING.format("batch_size, sequence_length"))
    @add_code_sample_docstrings(
        tokenizer_class=_TOKENIZER_FOR_DOC,
        checkpoint="xlm-mlm-en-2048",
        output_type=TFXLMWithLMHeadModelOutput,
        config_class=_CONFIG_FOR_DOC,
    )
    def call(self, inputs, **kwargs):
        return_dict = kwargs.get("return_dict")
        return_dict = return_dict if return_dict is not None else self.transformer.return_dict
        transformer_outputs = self.transformer(inputs, **kwargs)

        output = transformer_outputs[0]
        outputs = self.pred_layer(output)

        if not return_dict:
            return (outputs,) + transformer_outputs[1:]

        return TFXLMWithLMHeadModelOutput(
            logits=outputs, hidden_states=transformer_outputs.hidden_states, attentions=transformer_outputs.attentions
        )
