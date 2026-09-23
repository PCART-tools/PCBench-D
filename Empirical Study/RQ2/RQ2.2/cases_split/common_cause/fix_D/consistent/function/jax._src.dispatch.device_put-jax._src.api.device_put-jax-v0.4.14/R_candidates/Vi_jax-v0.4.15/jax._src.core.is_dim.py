def is_dim(v: Any) -> bool:
  return is_symbolic_dim(v) or is_constant_dim(v)
