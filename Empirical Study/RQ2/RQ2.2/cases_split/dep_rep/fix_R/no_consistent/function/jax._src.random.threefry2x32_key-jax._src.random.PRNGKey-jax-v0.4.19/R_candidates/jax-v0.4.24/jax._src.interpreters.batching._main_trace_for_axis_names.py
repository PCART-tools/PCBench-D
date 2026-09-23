def _main_trace_for_axis_names(main_trace: core.MainTrace,
                               axis_name: Iterable[AxisName],
                               ) -> bool:
  # This function exists to identify whether a main trace corresponds to any of
  # the axis names used by a primitive. Axis names alone aren't enough because
  # axis names can shadow, so we use the main trace as a tag.
  return any(main_trace is core.axis_frame(n).main_trace for n in axis_name)
