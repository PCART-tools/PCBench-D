def create_token() -> Token:
  return wrap_singleton_ir_values(hlo.create_token())
