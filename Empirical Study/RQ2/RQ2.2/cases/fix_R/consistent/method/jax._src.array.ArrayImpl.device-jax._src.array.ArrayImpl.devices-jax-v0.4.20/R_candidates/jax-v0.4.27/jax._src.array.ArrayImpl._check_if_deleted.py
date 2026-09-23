  def _check_if_deleted(self):
    if self.is_deleted():
      raise RuntimeError(
          f"Array has been deleted with shape={self.aval.str_short()}.")
