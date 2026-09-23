  @property
  def block_until_ready(self):
    # Raise AttributeError for backward compatibility with hasattr() and getattr() checks.
    raise AttributeError(self,
      f"The 'block_until_ready' method is not available on {self._error_repr()}."
      f"{self._origin_msg()}")
