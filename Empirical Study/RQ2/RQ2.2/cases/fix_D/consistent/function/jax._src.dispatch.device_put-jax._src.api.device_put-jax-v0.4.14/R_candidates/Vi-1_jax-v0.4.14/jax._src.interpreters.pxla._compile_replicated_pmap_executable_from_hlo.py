def _compile_replicated_pmap_executable_from_hlo(
    hlo: ir.Module, pci, input_indices, in_shardings, handle_outs,
    compile_options, host_callbacks, has_unordered_effects, ordered_effects,
    jaxpr_debug_info):
  # Use the standard out_handler.
  execute_fun = pci.backend.compile_replicated(
      is_trivial=False, name=pci.name, computation=hlo,
      compile_options=compile_options, host_callbacks=host_callbacks,
      has_unordered_effects=has_unordered_effects,
      ordered_effects=ordered_effects, in_avals=pci.avals,
      in_indices=input_indices, in_shardings=in_shardings,
      kept_var_idx=set(range(len(pci.avals))), out_handler=handle_outs)
  # TODO(frostig): need `compile_replicated` to give us the XLA executable
  return PmapExecutable(None, lambda: execute_fun, None, pci.avals,
                        jaxpr_debug_info, None)
