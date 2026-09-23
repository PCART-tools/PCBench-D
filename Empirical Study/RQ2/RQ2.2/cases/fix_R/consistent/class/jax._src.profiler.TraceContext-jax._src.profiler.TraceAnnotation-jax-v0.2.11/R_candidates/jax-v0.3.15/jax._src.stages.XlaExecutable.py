class XlaExecutable(Executable):

  def xla_extension_executable(self) -> xla_extension.Executable:
    raise NotImplementedError("must override")

  def call(self, *args_flat) -> Sequence[Any]:
    raise NotImplementedError("must override")

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

  def cost_analysis(self) -> List[Dict[str, float]]:
    xla_ext_exe = self.xla_extension_executable()
    err_msg = ("cost analysis unsupported on current XLA backend: "
               f"{type(xla_ext_exe)}")
    if not hasattr(xla_ext_exe, "client"):
      raise NotImplementedError(err_msg)
    try:
      return [xla_extension.hlo_module_cost_analysis(xla_ext_exe.client, m)
              for m in xla_ext_exe.hlo_modules()]
    except xla_extension.XlaRuntimeError as e:
      msg, *_ = e.args
      if type(msg) is str and msg.startswith("UNIMPLEMENTED"):
        raise NotImplementedError(err_msg) from e
      else:
        raise

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
