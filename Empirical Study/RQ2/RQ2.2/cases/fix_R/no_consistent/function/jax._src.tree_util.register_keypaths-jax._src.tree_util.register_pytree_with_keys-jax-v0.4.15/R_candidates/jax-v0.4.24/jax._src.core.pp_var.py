def pp_var(v: Var, context: JaxprPpContext) -> str:
  if isinstance(v, (Literal, DropVar)): return str(v)
  return f"{context.var_names[v]}{v.suffix}"
