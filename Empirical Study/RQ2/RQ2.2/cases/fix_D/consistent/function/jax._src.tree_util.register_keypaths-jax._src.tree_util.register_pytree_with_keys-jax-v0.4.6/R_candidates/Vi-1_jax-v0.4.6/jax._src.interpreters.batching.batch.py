def batch(fun: lu.WrappedFun, axis_name: AxisName, axis_size,
          in_dims, out_dim_dests, main_type: Type[BatchTrace] = BatchTrace,
          spmd_axis_name: Optional[Tuple[AxisName, ...]] = None
          ) -> lu.WrappedFun:
  # we split up _batch_inner and _batch_outer for the leak checker
  f = _batch_inner(fun, axis_size, out_dim_dests)
  return _batch_outer(f, axis_name, axis_size, in_dims, main_type,
                      spmd_axis_name)
