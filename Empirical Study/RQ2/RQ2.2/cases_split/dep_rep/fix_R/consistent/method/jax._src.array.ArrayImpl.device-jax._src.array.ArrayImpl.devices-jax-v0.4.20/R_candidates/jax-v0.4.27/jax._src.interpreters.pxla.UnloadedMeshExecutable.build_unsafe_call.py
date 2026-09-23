  def build_unsafe_call(self):
    if xla_extension_version >= 229:
      handle_args = InputsHandler(self.input_shardings)
    else:
      input_indices = _get_input_indices(self.input_avals, self.input_shardings,
                                         self.device_assignment)
      handle_args = InputsHandler(
          self.input_shardings, self.xla_executable.local_devices(), input_indices)
    handle_outs = global_avals_to_results_handler(
        self.output_avals, self.output_shardings, self.committed)  # type: ignore  # arg-type

    unsafe_call = ExecuteReplicated(  # type: ignore  # assignment
        self.xla_executable, self.name, self.backend, handle_args,
        handle_outs, self.unordered_effects, self.ordered_effects, self.keepalive,
        bool(self.host_callbacks), self.kept_var_idx, self.mut)
    return unsafe_call
