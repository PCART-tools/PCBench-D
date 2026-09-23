def _pjit_lower(
    jaxpr: core.ClosedJaxpr,
    in_shardings,
    out_shardings,
    *args, **kwargs):
  da = _fast_path_get_device_assignment(it.chain(in_shardings, out_shardings))
  in_shardings = SameDeviceAssignmentTuple(tuple(in_shardings), da)
  out_shardings = SameDeviceAssignmentTuple(tuple(out_shardings), da)
  return _pjit_lower_cached(jaxpr, in_shardings, out_shardings, *args, **kwargs)
