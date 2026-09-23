def wrap_singleton_ir_values(x: ir.Value | Sequence[ir.Value]
                             ) -> Sequence[ir.Value]:
  """Adds a consistent tuples to a mixture of tupled and untuple values."""
  return (x,) if isinstance(x, ir.Value) else tuple(x)
