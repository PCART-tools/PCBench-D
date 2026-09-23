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
