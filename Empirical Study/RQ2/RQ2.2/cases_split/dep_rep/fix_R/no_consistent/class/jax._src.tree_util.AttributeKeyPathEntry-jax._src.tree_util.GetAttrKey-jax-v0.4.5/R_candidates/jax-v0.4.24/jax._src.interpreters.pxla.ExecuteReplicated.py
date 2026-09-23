class ExecuteReplicated:
  """The logic to shard inputs, execute a replicated model, returning outputs."""
  __slots__ = ['xla_executable', 'name', 'backend', 'in_handler', 'out_handler',
               'has_unordered_effects', 'ordered_effects', 'keepalive',
               'has_host_callbacks', '_local_devices', 'kept_var_idx',
               '__weakref__']

  def __init__(self, xla_executable, name, backend, in_handler: InputsHandler,
               out_handler: ResultsHandler,
               unordered_effects: list[core.Effect],
               ordered_effects: list[core.Effect], keepalive: Any,
               has_host_callbacks: bool, kept_var_idx: set[int]):
    self.xla_executable = xla_executable
    self.name = name
    self.backend = backend
    self.in_handler = in_handler
    self.out_handler = out_handler
    self.has_unordered_effects = bool(unordered_effects)
    self.ordered_effects = ordered_effects
    self._local_devices = self.xla_executable.local_devices()
    self.keepalive = keepalive
    self.has_host_callbacks = has_host_callbacks
    self.kept_var_idx = kept_var_idx

  def _add_tokens_to_inputs(self, input_bufs):
    if self.ordered_effects:
      tokens = [
        dispatch.runtime_tokens.get_token_input(eff, self._local_devices)
        for eff in self.ordered_effects]
      input_bufs = [*tokens, *input_bufs]
    return input_bufs

  def _handle_token_bufs(self, token_bufs, sharded_token):
    # token_bufs: Sequence[Sequence[tokenArray]], for each effect the returned
    # token buffer (as a singleton list).
    # sharded_token: ShardedToken, containing the RuntimeTokens for each device
    for i, device in enumerate(self._local_devices):
      dispatch.runtime_tokens.set_output_runtime_token(
          device, sharded_token.get_token(i))
    for eff, token_buf in zip(self.ordered_effects, token_bufs):
      dispatch.runtime_tokens.set_token_result(eff, token_buf[0])

  @profiler.annotate_function
  def __call__(self, *args):
    args = [x for i, x in enumerate(args) if i in self.kept_var_idx]
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
      return self.out_handler(out_arrays)
    return results.consume_with_handlers(self.out_handler.handlers)
