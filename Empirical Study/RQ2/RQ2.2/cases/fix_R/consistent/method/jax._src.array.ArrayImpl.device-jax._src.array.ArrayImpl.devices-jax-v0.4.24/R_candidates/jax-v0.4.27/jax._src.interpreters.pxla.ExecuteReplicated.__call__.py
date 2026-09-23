  @profiler.annotate_function
  def __call__(self, *args):
    args = [x for i, x in enumerate(args) if i in self.kept_var_idx]
    if self.mut:
      args = [*args, *self.mut.in_mut]
    input_bufs = self.in_handler(args)
    if (self.ordered_effects or self.has_unordered_effects
        or self.has_host_callbacks):
      input_bufs = self._add_tokens_to_inputs(input_bufs)
      results = self.xla_executable.execute_sharded(
          input_bufs, with_tokens=True
      )
      result_token_bufs = results.disassemble_prefix_into_single_device_arrays(
          len(self.ordered_effects))
      sharded_runtime_token = results.consume_token()
      self._handle_token_bufs(result_token_bufs, sharded_runtime_token)
    else:
      results = self.xla_executable.execute_sharded(input_bufs)
    if dispatch.needs_check_special():
      out_arrays = results.disassemble_into_single_device_arrays()
      for arrays in out_arrays:
        dispatch.check_special(self.name, arrays)
      out = self.out_handler(out_arrays)
    else:
      out = results.consume_with_handlers(self.out_handler.handlers)
    if self.mut is None:
      return out
    else:
      out_ = []
      for i, o in zip(self.mut.out_mut, out):
        if i is not None:
          args[i]._buf = o
        else:
          out_.append(o)
      return out_
