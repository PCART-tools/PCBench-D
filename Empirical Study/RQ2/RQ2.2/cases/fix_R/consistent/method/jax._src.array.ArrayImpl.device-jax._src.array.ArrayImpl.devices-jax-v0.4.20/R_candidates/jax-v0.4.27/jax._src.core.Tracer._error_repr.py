  def _error_repr(self):
    if self.aval is None:
      return f"traced array with aval {self.aval}"
    return f"traced array with shape {raise_to_shaped(self.aval).str_short()}."
