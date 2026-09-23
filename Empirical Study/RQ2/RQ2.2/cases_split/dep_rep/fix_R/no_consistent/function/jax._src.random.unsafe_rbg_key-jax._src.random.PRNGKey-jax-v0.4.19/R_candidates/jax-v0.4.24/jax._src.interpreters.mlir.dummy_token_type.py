def dummy_token_type() -> Sequence[ir.Type]:
  # TODO(b/302258959): For now HLO does not allow hlo.TokenType among
  # arguments and results, so we use bool[0] to pass tokens to the
  # top-level function only.
  return aval_to_ir_types(core.ShapedArray((0,), np.bool_))
