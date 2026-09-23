    @property
    def dummy_inputs(self) -> Dict[str, tf.Tensor]:
        return getattr(self, self.base_model_prefix).dummy_inputs
