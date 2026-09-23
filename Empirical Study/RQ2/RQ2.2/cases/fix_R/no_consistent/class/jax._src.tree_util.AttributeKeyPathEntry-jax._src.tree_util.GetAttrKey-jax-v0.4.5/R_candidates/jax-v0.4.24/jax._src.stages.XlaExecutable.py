class XlaExecutable(Executable):

  def xla_extension_executable(self) -> xc.LoadedExecutable:
    raise NotImplementedError("must override")

  def call(self, *args_flat) -> Sequence[Any]:
    raise NotImplementedError("must override")

  def input_shardings(self) -> Sequence[jax.sharding.XLACompatibleSharding]:
    raise NotImplementedError(
        "compiled executable carries no input sharding information")

  def output_shardings(self) -> Sequence[jax.sharding.XLACompatibleSharding]:
    raise NotImplementedError(
        "compiled executable carries no output sharding information")

  def _input_layouts(self):
    raise NotImplementedError(
        "compiled executable carries no input layout information")

  def _output_layouts(self):
    raise NotImplementedError(
        "compiled executable carries no input layout information")

  def as_text(self) -> str:
    xla_ext_exe = self.xla_extension_executable()
    err_msg = ("text view unsupported on current XLA backend: "
               f"{type(xla_ext_exe)}")
    if not hasattr(xla_ext_exe, "hlo_modules"):
      raise NotImplementedError(err_msg)
    try:
      return "\n\n".join([m.to_string() for m in xla_ext_exe.hlo_modules()])
    except xla_extension.XlaRuntimeError as e:
      msg, *_ = e.args
      if type(msg) is str and msg.startswith("UNIMPLEMENTED"):
        raise NotImplementedError(err_msg) from e
      else:
        raise

    # TODO(skyewm): this should return a single dict (I think returning a list
    # was to support MPMD executables, which never fully landed)
  def cost_analysis(self) -> list[dict[str, float]]:
    xla_ext_exe = self.xla_extension_executable()

    # TODO(b/259255524): Unify/merge the two cost_analysis calls below.
    if hasattr(xla_ext_exe, "cost_analysis"):
      try:
        return [xla_ext_exe.cost_analysis()]
      except xla_extension.XlaRuntimeError as e:
        msg, *_ = e.args
        if not (type(msg) is str and msg.startswith("UNIMPLEMENTED")):
          raise

    # Try client method if executable cost_analysis method is unimplemented
    if hasattr(xla_ext_exe, "client"):
      try:
        return [
            xla_extension.hlo_module_cost_analysis(xla_ext_exe.client, m)
            for m in xla_ext_exe.hlo_modules()
        ]
      except xla_extension.XlaRuntimeError as e:
        msg, *_ = e.args
        if not (type(msg) is str and msg.startswith("UNIMPLEMENTED")):
          raise

    if (
        xla_ext_exe is None
        and hasattr(self, "unsafe_call")
        and hasattr(self.unsafe_call, "compiled")
        and hasattr(self.unsafe_call.compiled, "cost_analysis")
    ):
      return [self.unsafe_call.compiled.cost_analysis()]

    raise NotImplementedError(
        f"cost analysis unsupported on current XLA backend: {type(xla_ext_exe)}"
    )

  def memory_analysis(self) -> Any:
    xla_ext_exe = self.xla_extension_executable()
    err_msg = ("memory analysis unsupported on current XLA backend: "
               f"{type(xla_ext_exe)}")
    if not hasattr(xla_ext_exe, "get_compiled_memory_stats"):
      raise NotImplementedError(err_msg)
    try:
      return xla_ext_exe.get_compiled_memory_stats()
    except xla_extension.XlaRuntimeError as e:
      msg, *_ = e.args
      if type(msg) is str and msg.startswith("UNIMPLEMENTED"):
        raise NotImplementedError(err_msg) from e
      else:
        raise

  def runtime_executable(self) -> Any:
    return self.xla_extension_executable()
