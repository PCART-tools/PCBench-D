class XlaCompiledComputation(stages.XlaExecutable):
  def __init__(self, xla_executable, in_avals, kept_var_idx, unsafe_call,
               keepalive: Any):
    self._xla_executable = xla_executable
    self.in_avals = in_avals
    self._kept_var_idx = kept_var_idx
    self.unsafe_call = unsafe_call
    # Only the `unsafe_call` function is cached, so to avoid the `keepalive`
    # being garbage collected we attach it to `unsafe_call`.
    self.unsafe_call.keepalive = keepalive

  @staticmethod
  def from_xla_computation(name: str, xla_computation: Optional[ir.Module],
                           in_type: Optional[pe.InputType],
                           out_type: Optional[pe.OutputType], nreps: int,
                           device: Optional[Device], backend: Backend,
                           tuple_args: bool,
                           in_avals: Sequence[core.AbstractValue],
                           out_avals: Sequence[core.AbstractValue],
                           has_unordered_effects: bool,
                           ordered_effects: List[core.Effect],
                           kept_var_idx: Set[int], keepalive: Optional[Any],
                           host_callbacks: List[Any]) -> XlaCompiledComputation:
    sticky_device = device
    input_handler = _input_handler(backend, in_type, out_type)
    result_handler = _result_handler(backend, sticky_device, out_type)
    options = xb.get_compile_options(
        num_replicas=nreps, num_partitions=1,
        device_assignment=(sticky_device,) if sticky_device else None)
    options.parameter_is_tupled_arguments = tuple_args
    with log_elapsed_time(f"Finished XLA compilation of {name} "
                          "in {elapsed_time} sec"):
      compiled = compile_or_get_cached(backend, xla_computation, options,
                                       host_callbacks)
    buffer_counts = [aval_to_num_buffers(aval) for aval in out_avals]
    if ordered_effects or has_unordered_effects:
      num_output_tokens = len(ordered_effects) + has_unordered_effects
      buffer_counts = ([1] * num_output_tokens) + buffer_counts
    execute = _execute_compiled if nreps == 1 else _execute_replicated
    unsafe_call = partial(execute, name, compiled, input_handler, buffer_counts,  # type: ignore  # noqa: F811
                          result_handler, has_unordered_effects,
                          ordered_effects, kept_var_idx)
    return XlaCompiledComputation(compiled, in_avals, kept_var_idx, unsafe_call,
                                  keepalive)

  def is_trivial(self):
    return self._xla_executable == None

  @property
  def xla_executable(self):
    # TODO(frostig): remove in favor of runtime_executable?
    if self.is_trivial():
      raise ValueError("A trivial compiled computation has no XLA executable")
    return self._xla_executable

  @staticmethod
  def from_trivial_jaxpr(jaxpr, consts, device, in_avals, out_avals,
                         has_unordered_effects, ordered_effects, kept_var_idx,
                         keepalive: Optional[Any],
                         host_callbacks: List[Any]) -> XlaCompiledComputation:
    assert keepalive is None
    result_handlers = map(partial(aval_to_result_handler, device), out_avals)
    unsafe_call = partial(_execute_trivial, jaxpr, device, consts, out_avals,
                          result_handlers, has_unordered_effects,
                          ordered_effects, kept_var_idx, host_callbacks)
    return XlaCompiledComputation(None, in_avals, kept_var_idx, unsafe_call,
                                  keepalive)

  # -- stages.XlaExecutable overrides

  def xla_extension_executable(self):
    return self.xla_executable

  def call(self, *args):
    arg_specs = unsafe_map(arg_spec, args)
    arg_avals = [spec[0] for i, spec in enumerate(arg_specs)
                 if i in self._kept_var_idx]
    check_arg_avals_for_call(self.in_avals, arg_avals)
    return self.unsafe_call(*args)
