def gensym(jaxprs: Iterable[Jaxpr] | None = None,
           suffix: str = '') -> Callable[[AbstractValue], Var]:
  """Produce distinct variables, printed with the optional suffix.

  If `jaxprs` is provided, the variables produced will be distinct from those in
  any of the given jaxprs.
  """
  if jaxprs is None:
    start = 0
  else:
    all_vars = it.chain.from_iterable(_jaxpr_vars(j) for j in jaxprs)
    start = 1 + max((v.count for v in all_vars), default=-1)
  counter = it.count(start=start)
  return lambda aval: Var(next(counter), suffix, aval)
