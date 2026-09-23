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
