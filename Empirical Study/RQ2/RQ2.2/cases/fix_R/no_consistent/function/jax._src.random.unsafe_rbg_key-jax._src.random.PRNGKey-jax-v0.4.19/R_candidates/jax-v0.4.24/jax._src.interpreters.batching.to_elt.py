def to_elt(trace: Trace, get_idx: GetIdx, x: Vmappable, spec: MapSpec) -> Elt:
  handler = to_elt_handlers.get(type(x))
  if handler:
    return handler(partial(to_elt, trace, get_idx), get_idx, x, spec)
  elif type(x) is Jumble:
    if spec is not jumble_axis:
      raise TypeError("jumble input without using jumble_axis in_axes spec")
    ias: IndexedAxisSize  # Not present in the AxisSize union in core.py
    (d, ias), = ((i, sz)  # type: ignore
                 for i, sz in enumerate(x.aval.elt_ty.shape)
                 if type(sz) is IndexedAxisSize)
    batch_axis = make_batch_axis(x.data.ndim, 0, [(d+1, ias.lengths)])
    return BatchTracer(trace, x.data, batch_axis)  # type: ignore
  elif isinstance(spec, int) or spec is None:
    spec = spec and canonicalize_axis(spec, len(np.shape(x)))
    return (BatchTracer(trace, x, spec, source_info_util.current())
            if spec is not None else x)
  else:
    assert False
