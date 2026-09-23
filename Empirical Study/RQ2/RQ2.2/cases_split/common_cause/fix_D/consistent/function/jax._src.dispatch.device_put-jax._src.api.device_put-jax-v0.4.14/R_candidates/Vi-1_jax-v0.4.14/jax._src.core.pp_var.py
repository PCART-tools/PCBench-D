def pp_var(v: Var, context: JaxprPpContext) -> str:
  if isinstance(v, (Literal, DropVar)): return str(v)
  return f"{_encode_digits_alphabetic(context.var_ids[v])}{v.suffix}"
