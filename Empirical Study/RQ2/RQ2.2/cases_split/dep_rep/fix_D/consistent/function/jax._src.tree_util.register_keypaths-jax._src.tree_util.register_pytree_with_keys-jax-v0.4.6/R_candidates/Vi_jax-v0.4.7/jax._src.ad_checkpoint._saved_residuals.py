def _saved_residuals(jaxpr, arg_info) -> List[Tuple[core.AbstractValue, str]]:
  res_lits = [x for x in jaxpr.outvars if     isinstance(x, core.Literal)]
  res_vars = {x for x in jaxpr.outvars if not isinstance(x, core.Literal)}

  results = []

  for x in res_lits:
    results.append((x.aval, 'from a literal'))

  for v in jaxpr.constvars:
    if v in res_vars:
      results.append((v.aval, 'from a constant'))

  for i, v in enumerate(jaxpr.invars):
    if v in res_vars:
      if arg_info is not None:
        arg_name, arg_path = arg_info[i]
        src = f'from the argument {arg_name}{keystr(arg_path)}'
      else:
        src = 'from the argument at flattened index {i}'
      results.append((v.aval, src))

  for eqn in jaxpr.eqns:
    src = source_info_util.summarize(eqn.source_info)
    for v in eqn.outvars:
      if v in res_vars:
        if eqn.primitive is name_p:
          results.append((v.aval, f"named '{eqn.params['name']}' from {src}"))
        elif str(eqn.primitive) == 'xla_call':
          results.append((v.aval,
                          f"output of jitted function '{eqn.params['name']}' "
                          f"from {src}"))
        else:
          results.append((v.aval, f'output of {eqn.primitive.name} from {src}'))

  assert len(results) == len(jaxpr.outvars)
  return results
