  @property
  def copy_to_host_async(self):
    # Raise AttributeError for backward compatibility with hasattr() and getattr() checks.
    raise AttributeError(self,
      f"The 'copy_to_host_async' method is not available on {self._error_repr()}."
      f"{self._origin_msg()}")
