def batch_jaxpr2(
    closed_jaxpr: core.ClosedJaxpr,
    axis_size: core.AxisSize,
    in_axes: tuple[int | NotMapped | RaggedAxis, ...],
    axis_name: AxisName,
    spmd_axis_name: AxisName,
    main_type: type[BatchTrace],
  ) -> tuple[core.ClosedJaxpr, tuple[int | NotMapped | RaggedAxis, ...]]:
  # This is only ever used in pjit.  The difference vs batch_jaxpr is that
  # batch_jaxpr2 lets the callee decide which outputs are batched and what
  # their batch axes are; whereas batch_jaxpr has to obey caller-imposed
  # consistency constraints, such as type-agreement across arms of a
  # `lax.cond`, or input-output agreement for the body of a `lax.scan`.
  return _batch_jaxpr2(closed_jaxpr, axis_size, tuple(in_axes), axis_name,
                       spmd_axis_name, main_type)
