def local_avals_to_results_handler(
    unmapped_local_out_avals: Sequence[ShapedArray],
    local_shardings: Sequence[sharding_impls.XLACompatibleSharding]) -> ResultsHandler:
  out_indices = [tuple(s.devices_indices_map(aval.shape).values())
                 for s, aval in safe_zip(local_shardings, unmapped_local_out_avals)]
  handlers = [
      local_aval_to_result_handler(aval, s, idcs)
      for aval, s, idcs in safe_zip(unmapped_local_out_avals, local_shardings, out_indices)
  ]
  return ResultsHandler(handlers, local_shardings, unmapped_local_out_avals)
