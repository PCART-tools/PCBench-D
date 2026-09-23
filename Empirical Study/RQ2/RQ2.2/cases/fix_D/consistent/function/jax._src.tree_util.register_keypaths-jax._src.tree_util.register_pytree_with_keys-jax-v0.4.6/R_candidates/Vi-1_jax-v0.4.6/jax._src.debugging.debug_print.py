def debug_print(fmt: str, *args, ordered: bool = False, **kwargs) -> None:
  """Prints values and works in staged out JAX functions.

  Note: This function does *not* work with f-strings because the formatting is
  done lazily.

  Args:
    fmt: A format string, e.g. ``"hello {x}"``, that will be used to format
      input arguments.
    *args: A list of positional arguments to be formatted.
    ordered: A keyword only argument used to indicate whether or not the
      staged out computation will enforce ordering of this ``debug_print``
      w.r.t. other ordered ``debug_print`` calls.
    **kwargs: Additional keyword arguments to be formatted.
  """
  # Check that we provide the correct arguments to be formatted
  formatter.format(fmt, *args, **kwargs)

  debug_callback(functools.partial(_format_print_callback, fmt), *args,
                 **kwargs, ordered=ordered)
