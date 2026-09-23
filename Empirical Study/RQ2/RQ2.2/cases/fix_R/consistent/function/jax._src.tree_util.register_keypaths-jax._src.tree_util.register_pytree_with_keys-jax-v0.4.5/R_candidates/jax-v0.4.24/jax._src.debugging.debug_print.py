def debug_print(fmt: str, *args, ordered: bool = False, **kwargs) -> None:
  """Prints values and works in staged out JAX functions.

  This function does *not* work with f-strings because formatting is delayed.
  So instead of ``jax.debug.print(f"hello {bar}")``, write
  ``jax.debug.print("hello {bar}", bar=bar)``.

  This function is a thin convenience wrapper around :func:`jax.debug.callback`.
  The implementation is essentially::

    def debug_print(fmt: str, *args, **kwargs):
      jax.debug.callback(
          lambda *args, **kwargs: print(fmt.format(*args, **kwargs)),
          *args, **kwargs)

  It may be useful to call :func:`jax.debug.callback` directly instead of this
  convenience wrapper. For example, to get debug printing in logs, you might
  use :func:`jax.debug.callback` together with ``logging.log``.

  Args:
    fmt: A format string, e.g. ``"hello {x}"``, that will be used to format
      input arguments, like ``str.format``. See the Python docs on
      `string formatting <https://docs.python.org/3/library/stdtypes.html#str.format>`_
      and `format string syntax <https://docs.python.org/3/library/string.html#formatstrings>`_.
    *args: A list of positional arguments to be formatted, as if passed to
      ``fmt.format``.
    ordered: A keyword only argument used to indicate whether or not the
      staged out computation will enforce ordering of this ``jax.debug.print``
      w.r.t. other ordered ``jax.debug.print`` calls.
    **kwargs: Additional keyword arguments to be formatted, as if passed to
      ``fmt.format``.
  """
  # Check that we provide the correct arguments to be formatted
  formatter.format(fmt, *args, **kwargs)

  debug_callback(functools.partial(_format_print_callback, fmt), *args,
                 **kwargs, ordered=ordered)
