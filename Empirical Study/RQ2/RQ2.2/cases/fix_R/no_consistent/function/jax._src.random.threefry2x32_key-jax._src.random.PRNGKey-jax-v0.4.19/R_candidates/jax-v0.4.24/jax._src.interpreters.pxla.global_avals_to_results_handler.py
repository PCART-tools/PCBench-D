def global_avals_to_results_handler(
    global_out_avals: Sequence[ShapedArray],
    shardings: Sequence[sharding_impls.XLACompatibleSharding],
    committed: bool,
    are_out_shardings_from_xla: Sequence[bool]) -> ResultsHandler:
  handlers = [
      global_aval_to_result_handler(global_aval, s, committed, x)
      for global_aval, s, x in safe_zip(global_out_avals, shardings,
                                        are_out_shardings_from_xla)
  ]
  return ResultsHandler(handlers, shardings, global_out_avals)
