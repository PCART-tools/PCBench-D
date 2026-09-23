def collect_eqns(jaxpr: core.Jaxpr, key: Callable):
  d = collections.defaultdict(list)
  for _, eqn in all_eqns(jaxpr):
    d[key(eqn)].append(eqn)
  return dict(d)
