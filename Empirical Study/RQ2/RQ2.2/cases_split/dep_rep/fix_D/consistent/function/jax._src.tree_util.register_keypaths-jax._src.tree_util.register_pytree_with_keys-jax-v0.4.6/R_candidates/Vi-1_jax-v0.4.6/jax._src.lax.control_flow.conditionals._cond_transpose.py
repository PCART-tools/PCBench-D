def _cond_transpose(reduce_axes, cts, *args, branches, linear):
  del linear  # could use for error checking, but see #14026
  index, *ops = args
  linear = [type(x) is ad.UndefinedPrimal for x in ops]
  in_avals = map(raise_to_shaped, branches[0].in_avals)
  num_res = len(ops) - sum(linear)
  if any(isinstance(eff, state.RefEffect) for branch in branches for eff in
      branch.jaxpr.effects):
    raise NotImplementedError("State effect not supported in cond transpose.")

  branches_trans = tuple(
      _transpose_cond_jaxpr(jaxpr, num_res, reduce_axes) for jaxpr in branches)
  lin_in_avals = [raise_to_shaped(a, weak_type=False)
                  for a, l in zip(in_avals, linear) if l]
  assert all(core.typematch(out_aval, lin_in_aval)
             for jaxpr in branches_trans
             for out_aval, lin_in_aval in zip(jaxpr.out_avals, lin_in_avals))

  res = ops[:num_res]
  cts = map(ad.instantiate_zeros_aval, branches[0].out_avals, cts)
  linear_trans = (False,) * num_res + (True,) * len(cts)

  out = cond_p.bind(
      index, *res, *cts, branches=branches_trans, linear=linear_trans)
  assert all(map(core.typecheck, lin_in_avals, out))

  out_iter = iter(out)
  out = [next(out_iter) if l else None for l in linear]
  assert next(out_iter, None) is None
  return [None] + out
