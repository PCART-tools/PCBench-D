    def prepare_inputs_for_generation(self, inputs, **kwargs):
        """
        Implement in subclasses of :class:`~transfomers.TFPreTrainedModel` for custom behavior to prepare inputs in the
        generate method.
        """
        return {"inputs": inputs}
