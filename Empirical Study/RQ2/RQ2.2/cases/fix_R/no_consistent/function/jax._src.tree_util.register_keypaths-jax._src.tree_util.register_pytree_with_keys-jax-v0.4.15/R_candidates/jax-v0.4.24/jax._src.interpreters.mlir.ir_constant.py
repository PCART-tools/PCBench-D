def ir_constant(val: Any) -> ir.Value:
  """Convenience wrapper around ir_constants for singleton values."""
  values = ir_constants(val)
  if len(values) != 1:
    raise TypeError(f"ir_constant called on {val} which corresponds to "
                    f"multiple IR values {values}")
  return values[0]
