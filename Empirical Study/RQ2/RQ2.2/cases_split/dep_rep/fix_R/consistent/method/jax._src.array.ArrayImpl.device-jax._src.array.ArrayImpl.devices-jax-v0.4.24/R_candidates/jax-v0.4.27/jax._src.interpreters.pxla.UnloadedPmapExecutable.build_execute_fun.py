  def build_execute_fun(self):
    input_indices = []
    for aval, spec in safe_zip(self.local_input_avals, self.input_shardings):
      assert isinstance(spec, sharding_impls.PmapSharding), spec
      assert isinstance(aval, core.ShapedArray), aval
      input_indices.append(
          sharding_specs.spec_to_indices(aval.shape, spec.sharding_spec)
          if spec.sharding_spec is not None else None)
    handle_outs = local_avals_to_results_handler(self.local_output_avals,
                                                 self.output_shardings)
    handle_args = InputsHandler(self.input_shardings,
                                self.compiled.local_devices(), input_indices)
    execute_fun = ExecuteReplicated(self.compiled, "parallel computation",
                                    self.backend, handle_args, handle_outs,
                                    self.unordered_effects,
                                    self.ordered_effects, self.keepalive,
                                    bool(self.host_callbacks),
                                    set(range(len(input_indices))), None)
    return execute_fun
