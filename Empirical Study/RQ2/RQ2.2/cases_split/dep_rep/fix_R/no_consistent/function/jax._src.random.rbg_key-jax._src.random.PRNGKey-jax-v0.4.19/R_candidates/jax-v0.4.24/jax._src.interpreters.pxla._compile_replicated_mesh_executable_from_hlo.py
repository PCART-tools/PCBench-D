@weakref_lru_cache
def _compile_replicated_mesh_executable_from_hlo(
    computation, name, global_in_avals, global_out_avals, semantics_in_shardings,
    semantics_out_shardings, auto_spmd_lowering, compile_options,
    host_callbacks, has_unordered_effects, ordered_effects, kept_var_idx,
    backend, da, committed, pmap_nreps):
  assert not auto_spmd_lowering
  in_shardings = semantics_in_shardings.shardings
  out_shardings = semantics_out_shardings.shardings

  kept_var_idx = set(kept_var_idx)
  # Will compute out_handler with executable information.
  unsafe_call = backend.compile_replicated(
      is_trivial=False, name=name, computation=computation,
      compile_options=compile_options, host_callbacks=host_callbacks,
      has_unordered_effects=has_unordered_effects,
      device_assignment=da, ordered_effects=ordered_effects,
      in_avals=global_in_avals,
      in_shardings=in_shardings, kept_var_idx=kept_var_idx,
      out_avals=global_out_avals, out_shardings=out_shardings,
      committed=committed, pmap_nreps=pmap_nreps)
  xla_executable = None
  return MeshExecutable(xla_executable, lambda: unsafe_call, global_in_avals,
                        in_shardings, out_shardings, auto_spmd_lowering,
                        kept_var_idx, (None,) * len(global_in_avals),
                        (None,) * len(global_out_avals))
