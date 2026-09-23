  def get_aval(self) -> AbstractValue:
    """Get AbstractValue directly (if unknown) or from the constant (known)."""
    known = self.get_known()
    if known is not None:
      return get_aval(known)
    else:
      return self[0]
