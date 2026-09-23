@cache()
def _initial_style_jaxprs_with_common_consts(
    funs: Sequence[Callable], in_tree, in_avals, primitive_name: str):
  # When staging the branches of a conditional into jaxprs, constants are
  # extracted from each branch and converted to jaxpr arguments. To use the
  # staged jaxprs as the branches to a conditional *primitive*, we need for
  # their (input) signatures to match. This function "joins" the staged jaxprs:
  # for each one, it makes another that accepts *all* constants, but only uses
  # those that it needs (dropping the rest).

  jaxprs, all_consts, all_out_trees = \
      unzip3(_initial_style_open_jaxpr(fun, in_tree, in_avals, primitive_name)
             for fun in funs)

  newvar = core.gensym(jaxprs, suffix='_')
  all_const_avals = [map(_abstractify, consts) for consts in all_consts]
  unused_const_vars = [map(newvar, const_avals)
                       for const_avals in all_const_avals]
  def pad_jaxpr_constvars(i, jaxpr):
    prefix = util.concatenate(unused_const_vars[:i])
    suffix = util.concatenate(unused_const_vars[i + 1:])
    constvars = [*prefix, *jaxpr.constvars, *suffix]
    return jaxpr.replace(constvars=constvars)

  consts = util.concatenate(all_consts)
  jaxprs = [pad_jaxpr_constvars(i, jaxpr) for i, jaxpr in enumerate(jaxprs)]
  closed_jaxprs = [core.ClosedJaxpr(pe.convert_constvars_jaxpr(jaxpr), ())
                   for jaxpr in jaxprs]
  return closed_jaxprs, consts, all_out_trees
