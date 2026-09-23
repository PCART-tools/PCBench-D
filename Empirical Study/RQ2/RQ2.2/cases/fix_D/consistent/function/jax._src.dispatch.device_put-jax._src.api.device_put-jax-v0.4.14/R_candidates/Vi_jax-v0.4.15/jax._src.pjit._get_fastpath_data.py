def _get_fastpath_data(executable, out_tree, args_flat, out_flat):
  use_fastpath = (
      executable is not None and
      isinstance(executable, pxla.MeshExecutable) and
      isinstance(executable.unsafe_call, pxla.ExecuteReplicated) and
      # No effects in computation
      not executable.unsafe_call.ordered_effects and
      not executable.unsafe_call.has_unordered_effects and
      not executable.unsafe_call.has_host_callbacks and
      all(isinstance(x, xc.ArrayImpl) for x in out_flat)
  )

  if use_fastpath:
    out_avals = [o.aval for o in out_flat]
    out_committed = [o._committed for o in out_flat]
    kept_var_bitvec = [i in executable._kept_var_idx
                       for i in range(len(args_flat))]
    fastpath_data = pxla.MeshExecutableFastpathData(
        executable.xla_executable, out_tree, executable._in_shardings,
        executable._out_shardings, out_avals, out_committed, kept_var_bitvec)
  else:
    fastpath_data = None
  return fastpath_data
