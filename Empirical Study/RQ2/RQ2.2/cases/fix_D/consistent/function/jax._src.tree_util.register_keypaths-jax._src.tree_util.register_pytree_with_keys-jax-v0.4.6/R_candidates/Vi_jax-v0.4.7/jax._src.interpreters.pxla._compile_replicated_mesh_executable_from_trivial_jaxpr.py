def _compile_replicated_mesh_executable_from_trivial_jaxpr(
    jaxpr, consts, global_in_avals, global_out_avals, in_shardings, backend,
    device_assignment, committed, kept_var_idx, pmap_nreps):
  out_shardings = _out_shardings_for_trivial(
      jaxpr, consts, in_shardings, device_assignment)

  input_indices = _get_input_indices(
      global_in_avals, in_shardings)  # type: ignore
  handle_outs = global_avals_to_results_handler(
      global_out_avals, out_shardings, committed,
      [False] * len(global_out_avals))
  # Use the standard out_handler.
  unsafe_call = backend.compile_replicated(
      is_trivial=True, jaxpr=jaxpr, consts=consts,
      device_assignment=device_assignment, in_avals=global_in_avals,
      in_indices=input_indices, in_shardings=in_shardings,
      kept_var_idx=kept_var_idx, out_handler=handle_outs,
      out_shardings=out_shardings, pmap_nreps=pmap_nreps)
  return MeshExecutable(None, lambda: unsafe_call, global_in_avals,
                        in_shardings, out_shardings, False, kept_var_idx,
                        device_assignment, None)
