def _cond_batching_rule(axis_size, axis_name, main_type, args, dims, branches, linear):
  index, *ops = args
  index_dim, *op_dims = dims

  if index_dim is not batching.not_mapped:
    # Convert to a lax.select. While we could get away with not broadcasting
    # some operands yet, because all outputs must be broadcast together anyway
    # for the select we broadcast the input operands for simplicity and leave
    # optimizations to XLA.
    # TODO(mattjj,frostig): assumes branches are side-effect-free, revise!
    index, *ops = (
        batching.bdim_at_front(x, d, axis_size) for x, d in zip(args, dims))

    in_batched  = [True] * len(branches[0].in_avals)
    out_batched = [True] * len(branches[0].out_avals)

    branches_batched = [
        batching.batch_jaxpr(
            jaxpr, axis_size, in_batched, out_batched, axis_name, main_type)[0]
        for jaxpr in branches]

    branch_outs = []
    for i, jaxpr in enumerate(branches_batched):
      # Perform a select on the inputs for safety of reverse-mode autodiff; see
      # https://github.com/google/jax/issues/1052
      predicate = lax.eq(index, lax._const(index, i))
      ops_ = [_bcast_select(predicate, x, lax.stop_gradient(x)) for x in ops]
      branch_outs.append(core.jaxpr_as_fun(jaxpr)(*ops_))
    out = [_bcast_select_n(index, *outs) for outs in zip(*branch_outs)]
    return out, [0 if b else None for b in out_batched]
  else:
    ops_bat = [d is not batching.not_mapped for d in op_dims]
    ops = [batching.moveaxis(x, d, 0) if b else x
           for b, x, d in zip(ops_bat, ops, op_dims)]

    branches_out_bat = [
        batching.batch_jaxpr(jaxpr, axis_size, ops_bat, False, axis_name, main_type)[1]
        for jaxpr in branches]
    out_bat = [any(bat) for bat in zip(*branches_out_bat)]
    branches_batched = tuple(
        batching.batch_jaxpr(jaxpr, axis_size, ops_bat, out_bat, axis_name, main_type)[0]
        for jaxpr in branches)

    out_dims = [0 if b else batching.not_mapped for b in out_bat]
    out = cond_p.bind(
        index, *ops, branches=branches_batched, linear=linear)
    return out, out_dims
