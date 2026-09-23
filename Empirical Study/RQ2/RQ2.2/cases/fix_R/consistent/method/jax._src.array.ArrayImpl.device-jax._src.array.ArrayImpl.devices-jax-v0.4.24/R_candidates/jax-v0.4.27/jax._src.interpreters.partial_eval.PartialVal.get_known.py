  def get_known(self) -> core.Value | None:
    """Get the known value, if known, else None."""
    return self[1] if self[0] is None else None
