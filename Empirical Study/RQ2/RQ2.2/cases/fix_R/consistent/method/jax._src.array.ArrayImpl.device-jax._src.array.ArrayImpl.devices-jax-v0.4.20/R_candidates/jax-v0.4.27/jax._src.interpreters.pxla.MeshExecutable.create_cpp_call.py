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
        in_shardings = [
            a.dtype._rules.physical_sharding(a, s)
            if a is not core.abstract_token and dtypes.issubdtype(a.dtype, dtypes.extended)
            else s
            for s, a in zip(self._in_shardings, self.in_avals)
        ]
        fastpath_data = MeshExecutableFastpathData(
            self.xla_executable, out_tree_dispatch, in_shardings,
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
