  def starter_data(self, inputs: Sequence[np.ndarray]) -> CompatTestData:
    # Helper for starting a test, see module docstring.
    assert isinstance(inputs, Sequence), f"{inputs}"
    return dataclasses.replace(self.load_testdata(dummy_data_dict),
                               inputs=inputs,
                               platform=self.default_jax_backend())
