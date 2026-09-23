def pprof_equation_profile(jaxpr: core.Jaxpr) -> bytes:
  """Generates a pprof profile that maps jaxpr equations to Python stack traces.

  By visualizing the profile using pprof, one can identify Python code that is
  responsible for yielding large numbers of jaxpr equations.

  Args:
    jaxpr: a Jaxpr.

  Returns:
    A gzip-compressed pprof Profile protocol buffer, suitable for passing to
    pprof tool for visualization.
  """
  d = Counter(
      (eqn.source_info.traceback, eqn.primitive)
      for _, eqn in all_eqns(jaxpr)
  )
  return _pprof_profile(d)
