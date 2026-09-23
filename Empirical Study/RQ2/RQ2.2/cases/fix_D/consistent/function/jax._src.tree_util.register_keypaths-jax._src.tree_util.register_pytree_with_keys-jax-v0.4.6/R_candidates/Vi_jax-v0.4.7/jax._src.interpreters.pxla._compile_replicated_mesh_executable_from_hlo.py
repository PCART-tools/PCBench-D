def _compile_replicated_mesh_executable_from_hlo(
    name, computation, global_in_avals, global_out_avals, in_shardings,
    out_shardings, auto_spmd_lowering, compile_options,
    host_callbacks, has_unordered_effects, ordered_effects, kept_var_idx,
    backend, device_assignment, committed, pmap_nreps):
  assert not auto_spmd_lowering
  input_indices = _get_input_indices(
      global_in_avals, in_shardings)  # type: ignore
  if pmap_nreps > 1:
    # For a jit wrapping a pmap, replicate each input index to match the
    # devices of the replicated jit computation.
    input_indices = [index * pmap_nreps for index in input_indices]

  # Will compute out_handler with executable information.
  unsafe_call = backend.compile_replicated(
      is_trivial=False, name=name, computation=computation,
      compile_options=compile_options, host_callbacks=host_callbacks,
      has_unordered_effects=has_unordered_effects,
      ordered_effects=ordered_effects, in_avals=global_in_avals,
      in_indices=input_indices, in_shardings=in_shardings,
      kept_var_idx=kept_var_idx,
      out_avals=global_out_avals, out_shardings=out_shardings,
      committed=committed, pmap_nreps=pmap_nreps)
  xla_executable = None
  return MeshExecutable(xla_executable, lambda: unsafe_call, global_in_avals,
                        in_shardings, out_shardings, auto_spmd_lowering,
                        kept_var_idx, device_assignment, None)
