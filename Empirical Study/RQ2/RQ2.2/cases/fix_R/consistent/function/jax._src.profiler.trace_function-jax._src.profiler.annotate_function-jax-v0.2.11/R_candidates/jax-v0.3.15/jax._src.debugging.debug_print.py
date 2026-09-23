def debug_print(fmt: str, *args, ordered=False, **kwargs) -> None:
  """Prints values and works in staged out JAX functions.

  Args:
    fmt: A format string, e.g. `"hello {x}"`, that will be used to format
      input arguments.
    *args: A list of positional arguments to be formatted.
    ordered: A keyword only argument used to indicate whether or not the
      staged out computation will enforce ordering of this `debug_print` w.r.t.
      other ordered `debug_print`s.
    **kwargs: Additional keyword arguments to be formatted.
  """
  effect = DebugEffect.ORDERED_PRINT if ordered else DebugEffect.PRINT
  debug_callback(functools.partial(_format_print_callback, fmt), effect, *args,
                 **kwargs)
