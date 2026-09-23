  def __init__(self, xla_executable, build_unsafe_call, in_avals, out_avals,
               in_shardings, out_shardings, auto_spmd_lowering, kept_var_idx,
               in_layouts, out_layouts,
               all_args_info: AllArgsInfo | None = None,
               unloaded_executable=None):
    self.xla_executable = xla_executable
    self.build_unsafe_call = build_unsafe_call
    # in_avals is a list of global and local avals. Aval is global if input
    # is a GDA or jax.Array else local.
    self.in_avals = in_avals
    self.out_avals = out_avals
    self._unsafe_call = None
    self._in_shardings = in_shardings
    self._out_shardings = out_shardings
    self._auto_spmd_lowering = auto_spmd_lowering
    self._kept_var_idx = kept_var_idx
    self._in_layouts = in_layouts
    self._out_layouts = out_layouts
    self._all_args_info = all_args_info
    self._unloaded_executable = unloaded_executable
