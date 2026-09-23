  def matches(self, avals: Sequence[jax_core.ShapedArray]) -> bool:
    if len(avals) != len(self.arg_types):
      return False
    return all(
        aval.weak_type or aval.dtype.name == arg_type
        for aval, arg_type in zip(avals, self.arg_types)
    )
