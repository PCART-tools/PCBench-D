class MeshExecutable(stages.XlaExecutable):
  __slots__ = [
      "xla_executable", "_unsafe_call", "build_unsafe_call", "in_avals",
      "_in_shardings", "_out_shardings", "_auto_spmd_lowering", "_kept_var_idx",
      "_in_layouts", "_out_layouts", "_all_args_info", "_unloaded_executable",
  ]

  def __init__(self, xla_executable, build_unsafe_call, in_avals, in_shardings,
               out_shardings, auto_spmd_lowering, kept_var_idx,
               in_layouts, out_layouts,
               all_args_info: AllArgsInfo | None = None,
               unloaded_executable=None):
    self.xla_executable = xla_executable
    self.build_unsafe_call = build_unsafe_call
    # in_avals is a list of global and local avals. Aval is global if input
    # is a GDA or jax.Array else local.
    self.in_avals = in_avals
    self._unsafe_call = None
    self._in_shardings = in_shardings
    self._out_shardings = out_shardings
    self._auto_spmd_lowering = auto_spmd_lowering
    self._kept_var_idx = kept_var_idx
    self._in_layouts = in_layouts
    self._out_layouts = out_layouts
    self._all_args_info = all_args_info
    self._unloaded_executable = unloaded_executable

  @property
  def unsafe_call(self) -> Callable[..., Any]:
    if self._unsafe_call is None:
      self._unsafe_call = self.build_unsafe_call()
    return self._unsafe_call  # type: ignore

  # -- stages.XlaExecutable overrides

  def xla_extension_executable(self):
    return self.xla_executable

  def call(self, *args):
    if self._all_args_info is None:
      kept_args = [a for i, a in enumerate(args) if i in self._kept_var_idx]
      ref_avals = self.in_avals
      in_shardings = self._in_shardings
      debug_info = None
    else:
      kept_args = args
      ref_avals = self._all_args_info.in_avals
      iter_in_shardings = iter(self._in_shardings)
      in_shardings = [next(iter_in_shardings) if i in self._kept_var_idx else s
                      for i, s in enumerate(self._all_args_info.in_shardings)]
      debug_info = self._all_args_info.debug_info

    arg_avals = map(xla.abstractify, kept_args)
    check_arg_avals_for_call(ref_avals, arg_avals, debug_info)
    # Check the GDA sharding and the input sharding.
    check_gda_or_array_xla_sharding_match(kept_args, in_shardings, debug_info)
    return self.unsafe_call(*args)  # pylint: disable=not-callable

  def input_shardings(self) -> Sequence[sharding_impls.XLACompatibleSharding]:
    return self._in_shardings

  def output_shardings(self) -> Sequence[sharding_impls.XLACompatibleSharding]:
    return self._out_shardings

  def input_layouts(self):
    return self._in_layouts

  def output_layouts(self):
    return self._out_layouts

  def create_cpp_call(self, no_kwargs, in_tree, out_tree):
    if not (isinstance(self.unsafe_call, ExecuteReplicated) and
            not self.unsafe_call.has_unordered_effects and
            not self.unsafe_call.has_host_callbacks):
      return None

    def aot_cache_miss(*args, **kwargs):
      params = stages.CompiledCallParams(self, no_kwargs, in_tree, out_tree)
      outs, out_flat, args_flat = stages.Compiled.call(params, *args, **kwargs)
      out_flat, out_tree_dispatch = reflatten_outputs_for_dispatch(
          out_tree, out_flat)
      use_fastpath = (all(isinstance(x, xc.ArrayImpl) for x in out_flat))

      if use_fastpath:
        out_avals = [o.aval for o in out_flat]
        out_committed = [o._committed for o in out_flat]
        kept_var_bitvec = [i in self._kept_var_idx
                           for i in range(len(args_flat))]
        fastpath_data = MeshExecutableFastpathData(
            self.xla_executable, out_tree_dispatch, self._in_shardings,
            self._out_shardings, out_avals, out_committed, kept_var_bitvec,
            self.unsafe_call.in_handler.local_devices,
            self.unsafe_call.in_handler.input_indices)
      else:
        fastpath_data = None
      return outs, fastpath_data

    if xla_extension_version >= 226:
      return xc._xla.pjit(
          self.unsafe_call.name, None, aot_cache_miss, [], [], [],
          tree_util.dispatch_registry,
          shard_arg if xla_extension_version >= 229 else temp_shard_arg)  # type: ignore
    else:
      return xc._xla.pjit(self.unsafe_call.name, None, aot_cache_miss, [], [], [],  # type: ignore
                          tree_util.dispatch_registry)
