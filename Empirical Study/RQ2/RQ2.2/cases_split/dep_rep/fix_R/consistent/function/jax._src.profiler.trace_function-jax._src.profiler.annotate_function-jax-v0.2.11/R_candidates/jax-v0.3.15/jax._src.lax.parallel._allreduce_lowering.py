def _allreduce_lowering(prim, pos_fn, ctx, *args, axes, axis_index_groups):
  if axis_index_groups is not None and ctx.module_context.platform == "tpu":
    len_0 = len(axis_index_groups[0])
    if any(len(g) != len_0 for g in axis_index_groups):
      raise ValueError("axis_index_groups must all be the same size")
  named_axes, positional_axes = axes_partition = [], []
  for axis in axes:
    axes_partition[isinstance(axis, int)].append(axis)

  if positional_axes:
    reducer = mlir.lower_fun(pos_fn, multiple_results=False)
    def _positional_reduce(aval, arg):
      aval_out = aval.update(
          shape=np.delete(np.array(aval.shape, dtype=np.int64),
                          positional_axes))
      reducer_ctx = ctx.replace(primitive=None, avals_in=[aval], avals_out=[aval_out])
      out, = reducer(reducer_ctx, arg, axes=tuple(positional_axes))[0]
      return out
    args = map(_positional_reduce, ctx.avals_in, args)
  if not named_axes:
    return args

  replica_groups = _replica_groups_mhlo(
      _replica_groups(ctx.module_context.axis_env, named_axes,
                      axis_index_groups))
  def all_reduce(x_dtype, x):
    op = mhlo.AllReduceOp(
        x.type, x, replica_groups=replica_groups, channel_handle=None)
    scalar_aval = core.ShapedArray((), x_dtype)
    scalar_type = mlir.aval_to_ir_type(scalar_aval)
    reducer_block = op.regions[0].blocks.append(scalar_type, scalar_type)
    with ir.InsertionPoint(reducer_block):
      lower_reducer = mlir.lower_fun(prim.bind, multiple_results=False)
      reducer_ctx = ctx.replace(primitive=None,
                                avals_in=[scalar_aval] * 2, avals_out=[scalar_aval])
      out_nodes = lower_reducer(
          reducer_ctx, *([a] for a in reducer_block.arguments))
      mhlo.ReturnOp(util.flatten(out_nodes))
    return op.result

  return [all_reduce(aval.dtype, x) for aval, x in zip(ctx.avals_in, args)]
