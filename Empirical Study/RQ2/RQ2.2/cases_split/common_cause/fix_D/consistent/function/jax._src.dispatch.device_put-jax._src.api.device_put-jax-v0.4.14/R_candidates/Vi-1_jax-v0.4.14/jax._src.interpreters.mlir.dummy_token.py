def dummy_token() -> Sequence[ir.Value]:
  return ir_constants(np.zeros(0, np.bool_))
