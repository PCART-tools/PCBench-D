@weakref_lru_cache
def _closed_jaxpr_partial_eval_custom_cached(
    jaxpr: ClosedJaxpr, unks_in: tuple[bool, ...], inst_in: tuple[bool, ...],
    dropvars: tuple[bool, ...], saveable: Callable
    ) -> tuple[ClosedJaxpr, ClosedJaxpr, Sequence[bool], Sequence[bool],
               int, int, Sequence[int | None]]:
  jaxpr_known_, jaxpr_staged_, unks_out, inst_out, num_res_val, num_res_ref = \
      partial_eval_jaxpr_stateful(jaxpr.jaxpr, unks_in, inst_in,
                                  False, False, saveable)

  # Compute which residual value outputs are also *undropped* primal outputs.
  num_out_primals = len(jaxpr_known_.outvars) - num_res_val
  out_vars, res_vars = split_list(jaxpr_known_.outvars, [num_out_primals])
  out_dropvars_known, _ = partition_list(unks_out, dropvars)
  idx_map = {id(v): i for i, (v, b) in enumerate(zip(out_vars, out_dropvars_known))
             if not b}
  out_fwd = [idx_map.get(id(v)) for v in res_vars]

  # Prune jaxpr_known_ outputs by removing forwards.
  jaxpr_known_ = prune_jaxpr_outputs(
      jaxpr_known_, [True] * num_out_primals + [f is None for f in out_fwd])

  jaxpr_known = core.ClosedJaxpr(jaxpr_known_, jaxpr.consts)
  jaxpr_staged = core.ClosedJaxpr(jaxpr_staged_, jaxpr.consts)
  return jaxpr_known, jaxpr_staged, unks_out, inst_out, num_res_ref, num_res_val, out_fwd
