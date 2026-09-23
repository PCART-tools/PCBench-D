def _substitute_vars_in_type(
    consts: dict[Var, Literal], env: dict[Var, Var], a: AbstractValue
  ) -> AbstractValue:
  if isinstance(a, DShapedArray) and any(isinstance(d, Var) for d in a.shape):
    shape = [consts[d].val if d in consts else env[d]  # type: ignore
             if isinstance(d, Var) else d for d in a.shape]
    return a.update(shape=tuple(shape))
  else:
    return a
