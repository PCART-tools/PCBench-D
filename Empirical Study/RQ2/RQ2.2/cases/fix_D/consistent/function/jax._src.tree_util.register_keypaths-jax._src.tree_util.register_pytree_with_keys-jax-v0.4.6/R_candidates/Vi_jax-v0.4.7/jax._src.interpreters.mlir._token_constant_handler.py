def _token_constant_handler(val, canonicalize_types):
  return [hlo.CreateTokenOp().result]
