def dummy_token_type() -> Sequence[ir.Type]:
  return aval_to_ir_types(core.ShapedArray((0,), np.bool_))
