def transpose_jaxpr(jaxpr: core.ClosedJaxpr, in_linear: bool | Sequence[bool],
                    out_zeros: bool | Sequence[bool],
                    reduce_axes: Sequence[core.AxisName],
                    ) -> tuple[core.ClosedJaxpr, list[bool]]:
  if type(in_linear) is bool:
    in_linear = (in_linear,) * len(jaxpr.in_avals)
  if type(out_zeros) is bool:
    out_zeros = (out_zeros,) * len(jaxpr.out_avals)
  return _transpose_jaxpr(jaxpr, tuple(in_linear), tuple(out_zeros),
                          tuple(reduce_axes))
