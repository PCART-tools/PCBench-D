def batch_custom_vjp_bwd(bwd, axis_name, axis_size, in_dims, out_dim_dests,
                         main_type, spmd_axis_name):
  def new_bwd(*args):
    in_dims_ = in_dims() if callable(in_dims) else in_dims
    args = [SymbolicZero(core.mapped_aval(axis_size, dim, x.aval))
            if type(x) is SymbolicZero else x
            for x, dim in zip(args, in_dims_)]
    in_dims_ = [None if type(x) is SymbolicZero else d
                for x, d in zip(args, in_dims_)]
    bwd_, out_dims_thunk = batch_subtrace(lu.wrap_init(bwd))
    bwd_ = _batch_outer(bwd_, axis_name, axis_size, in_dims_, main_type,
                        spmd_axis_name)
    bwd_ = _match_axes_and_sum(bwd_, axis_size, axis_name, out_dims_thunk,
                               out_dim_dests)
    return bwd_.call_wrapped(*args)
  return new_bwd
