    @add_start_docstrings_to_model_forward(LONGFORMER_INPUTS_DOCSTRING.format("batch_size, sequence_length"))
    def call(self, inputs, **kwargs):
        outputs = self.longformer(inputs, **kwargs)

        return outputs
