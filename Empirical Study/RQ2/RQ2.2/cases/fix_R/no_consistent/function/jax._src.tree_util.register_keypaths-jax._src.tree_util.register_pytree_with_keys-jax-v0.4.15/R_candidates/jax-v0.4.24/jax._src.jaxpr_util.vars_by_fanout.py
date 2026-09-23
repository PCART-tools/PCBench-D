def vars_by_fanout(jaxpr: core.Jaxpr):
  def fmt_key(var, eqn):
    if eqn is None:
      return f'{var} <- invar'
    else:
      src = source_info_util.summarize(eqn.source_info)
      return f'{var} <- {eqn.primitive.name} @ {src}'

  def hist(jaxpr, reads):
    return {fmt_key(var, var_def): len(var_refs)
            for var, var_def, var_refs in reads}

  return [(j, hist(j, reads)) for j, reads in var_defs_and_refs(jaxpr)]  # pytype: disable=bad-unpacking
