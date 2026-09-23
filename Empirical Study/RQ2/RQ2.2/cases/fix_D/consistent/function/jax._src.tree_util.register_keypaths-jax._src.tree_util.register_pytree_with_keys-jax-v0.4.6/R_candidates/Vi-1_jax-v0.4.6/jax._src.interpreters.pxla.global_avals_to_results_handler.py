def global_avals_to_results_handler(
    global_out_avals: Sequence[ShapedArray],
    shardings: Sequence[sharding_internal.XLACompatibleSharding],
    committed: bool,
    are_out_shardings_from_xla: Sequence[bool]) -> ResultsHandler:
  if config.jax_parallel_functions_output_gda or config.jax_array:
    handlers = [
        global_aval_to_result_handler(global_aval, s, committed, x)
        for global_aval, s, x in safe_zip(global_out_avals, shardings,
                                          are_out_shardings_from_xla)
    ]
    return ResultsHandler(handlers, shardings, global_out_avals)
  else:
    # This path is taken when the outputs are SDAs.
    assert all(isinstance(s, sharding_internal.NamedSharding) for s in shardings)
    local_out_avals = [s.mesh._global_to_local(get_array_mapping(s.spec), aval)
                       for aval, s in safe_zip(global_out_avals, shardings)]
    local_shardings = [sharding_internal.NamedSharding(s.mesh.local_mesh, s.spec)  # type: ignore
                       for s in shardings]
    return local_avals_to_results_handler(local_out_avals, local_shardings)
