def _batch_trace_process_xmap(self, is_spmd, primitive, f: lu.WrappedFun, tracers, params):
  not_mapped = batching.not_mapped
  vals, dims = unzip2((t.val, t.batch_dim) for t in tracers)
  assert primitive is xmap_p
  if not is_spmd and all(dim is not_mapped for dim in dims):
    return primitive.bind(f, *vals, **params)
  else:
    assert len({x.shape[d] for x, d in zip(vals, dims) if d is not not_mapped}) == 1
    new_in_axes = tuple(
      _fmap_dims(in_axes, lambda a: a + (d is not not_mapped and d <= a))
      for d, in_axes in zip(dims, params['in_axes']))
    mapped_dims_in = tuple(
      d if d is not_mapped else d - sum(a < d for a in in_axis.values())
      for d, in_axis in zip(dims, params['in_axes']))
    f, mapped_dims_out = batching.batch_subtrace(f, self.main, mapped_dims_in)
    out_axes_thunk: Callable[[], Sequence[AxisNamePos]] = params['out_axes_thunk']
    dims_out_thunk = lambda: tuple(d if d is not_mapped else _axis_after_insertion(d, out_axes)
                                   for d, out_axes in zip(mapped_dims_out(), out_axes_thunk()))
    # NOTE: This assumes that the choice of the dimensions over which outputs
    #       are batched is entirely dependent on the function and not e.g. on the
    #       data or its shapes.
    @as_hashable_function(closure=out_axes_thunk)
    def new_out_axes_thunk():
      return tuple(
        out_axes if d is not_mapped else
        _fmap_dims(out_axes, lambda a, nd=_axis_after_insertion(d, out_axes): a + (nd <= a))
        for out_axes, d in zip(out_axes_thunk(), mapped_dims_out()))

    if not is_spmd:
      assert params['spmd_in_axes'] is None and params['spmd_out_axes_thunk'] is None
      new_spmd_in_axes = None
      new_spmd_out_axes_thunk = None
    else:
      new_spmd_in_axes, new_spmd_out_axes_thunk = _batch_trace_update_spmd_axes(
        params['spmd_in_axes'], params['spmd_out_axes_thunk'],
        self.axis_name, dims, dims_out_thunk)

    new_params = dict(params,
                      in_axes=new_in_axes, out_axes_thunk=new_out_axes_thunk,
                      spmd_in_axes=new_spmd_in_axes,
                      spmd_out_axes_thunk=new_spmd_out_axes_thunk)
    vals_out = primitive.bind(f, *vals, **new_params)
    dims_out = dims_out_thunk()
    return [batching.BatchTracer(self, v, d) for v, d in zip(vals_out, dims_out)]
