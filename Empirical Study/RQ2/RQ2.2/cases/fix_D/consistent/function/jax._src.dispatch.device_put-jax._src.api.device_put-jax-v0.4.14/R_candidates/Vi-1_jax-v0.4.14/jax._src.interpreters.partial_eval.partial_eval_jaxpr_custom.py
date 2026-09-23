def partial_eval_jaxpr_custom(
    jaxpr: Jaxpr,
    in_unknowns: Sequence[bool],
    in_inst: bool | Sequence[bool],
    ensure_out_unknowns: bool | Sequence[bool],
    ensure_out_inst: bool | Sequence[bool],
    saveable: Callable[..., bool],
  ) -> tuple[Jaxpr, Jaxpr, list[bool], list[bool], int]:
  if type(in_inst) is bool:
    in_inst = (in_inst,) * len(jaxpr.invars)
  if type(ensure_out_unknowns) is bool:
    ensure_out_unknowns = (ensure_out_unknowns,) * len(jaxpr.outvars)
  if type(ensure_out_inst) is bool:
    ensure_out_inst = (ensure_out_inst,) * len(jaxpr.outvars)
  jaxpr_known, jaxpr_staged, out_unknowns, out_inst, num_res, num_res_ref = \
      _partial_eval_jaxpr_custom_cached(jaxpr, tuple(in_unknowns),
                                        tuple(in_inst),
                                        tuple(ensure_out_unknowns),
                                        tuple(ensure_out_inst), saveable)
  if num_res_ref > 0:
    raise ValueError(
        "Cannot use `partial_eval_jaxpr_custom` with stateful jaxprs.")
  return jaxpr_known, jaxpr_staged, out_unknowns, out_inst, num_res
