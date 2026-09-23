class _DebugPrintFormatChecker(string.Formatter):

  def check_unused_args(self, used_args, args, kwargs):
    unused_args = [arg for i, arg in enumerate(args) if i not in used_args]
    unused_kwargs = [k for k in kwargs if k not in used_args]
    if unused_args:
      raise ValueError(
          f"Unused positional arguments to `jax.debug.print`: {unused_args}")
    if unused_kwargs:
      raise ValueError(
          f"Unused keyword arguments to `jax.debug.print`: {unused_kwargs}. "
          "You may be passing an f-string (i.e, `f\"{x}\"`) into "
          "`jax.debug.print` and instead should pass in a regular string.")
