def typecheck(aval: AbstractValue, x) -> bool:
  return typecompat(aval, get_aval(x))
