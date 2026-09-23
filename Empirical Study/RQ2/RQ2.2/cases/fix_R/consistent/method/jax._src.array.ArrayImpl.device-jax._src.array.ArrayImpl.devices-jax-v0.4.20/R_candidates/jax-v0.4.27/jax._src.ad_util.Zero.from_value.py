  @staticmethod
  def from_value(val: Any) -> Zero:
    return Zero(raise_to_shaped(get_aval(val)))
