  def get_context(self, x):
    if isinstance(x, (np.ndarray, np.floating, np.complexfloating)):
      fp_format = str(x.dtype)
      fp_format = self.map_complex_to_float.get(fp_format, fp_format)
      return self.contexts[fp_format]
    raise NotImplementedError(f'get mpmath context from {type(x).__name__} instance')
