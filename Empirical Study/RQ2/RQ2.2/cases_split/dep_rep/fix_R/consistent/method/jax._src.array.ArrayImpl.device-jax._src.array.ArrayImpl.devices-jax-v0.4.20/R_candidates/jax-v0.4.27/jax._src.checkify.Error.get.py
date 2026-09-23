  def get(self) -> str | None:
    """Returns error message if error happened, None if no error happened."""
    exp = self.get_exception()
    if exp is not None:
      return str(exp)
    return None
