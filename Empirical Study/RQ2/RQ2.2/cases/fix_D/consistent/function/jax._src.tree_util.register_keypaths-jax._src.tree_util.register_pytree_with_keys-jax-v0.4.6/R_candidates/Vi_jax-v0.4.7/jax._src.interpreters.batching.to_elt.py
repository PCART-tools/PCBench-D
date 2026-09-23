def to_elt(trace: Trace, get_idx: GetIdx, x: Vmappable, spec: MapSpec) -> Elt:
  handler = to_elt_handlers.get(type(x))
  if handler:
    return handler(partial(to_elt, trace, get_idx), get_idx, x, spec)
  elif type(x) is Pile:
    if spec is not pile_axis:
      raise TypeError("pile input without using pile_axis in_axes spec")
    (d, ias), = ((i, sz) for i, sz in enumerate(x.aval.elt_ty.shape)
                 if type(sz) is IndexedAxisSize)
    return BatchTracer(trace, x.data, ConcatAxis(d, ias.lengths))  # type: ignore
  elif isinstance(spec, int) or spec is None:
    spec = spec and canonicalize_axis(spec, len(np.shape(x)))
    return (BatchTracer(trace, x, spec, source_info_util.current())
            if spec is not None else x)
  else:
    assert False
