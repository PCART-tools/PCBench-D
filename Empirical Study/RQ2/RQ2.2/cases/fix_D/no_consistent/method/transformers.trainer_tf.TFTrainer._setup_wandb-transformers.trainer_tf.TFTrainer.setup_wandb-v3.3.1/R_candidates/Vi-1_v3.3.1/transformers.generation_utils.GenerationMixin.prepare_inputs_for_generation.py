    def prepare_inputs_for_generation(self, input_ids, **kwargs):
        """
        Implement in subclasses of :class:`~transfomers.PreTrainedModel` for custom behavior to prepare inputs in the
        generate method.
        """
        return {"input_ids": input_ids}
