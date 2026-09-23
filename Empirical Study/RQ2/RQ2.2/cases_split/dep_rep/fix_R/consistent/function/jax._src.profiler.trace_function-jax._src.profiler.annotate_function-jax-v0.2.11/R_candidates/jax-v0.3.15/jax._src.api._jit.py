def _jit(
    use_cpp_jit: bool,
    fun: Callable,
    static_argnums: Union[int, Iterable[int], None] = None,
    static_argnames: Union[str, Iterable[str], None] = None,
    device: Optional[xc.Device] = None,
    backend: Optional[str] = None,
    donate_argnums: Union[int, Iterable[int]] = (),
    inline: bool = False,
    keep_unused: bool = False,
    abstracted_axes: Optional[Any] = None,
  ) -> stages.Wrapped:
  # Implemements common logic between CPP and Python backends
  _check_callable(fun)

  # Coerce input
  donate_argnums = _ensure_index_tuple(donate_argnums)

  try:
    sig = inspect.signature(fun)
  except ValueError:
    # Some built-in functions don't support signature.
    # See: https://github.com/python/cpython/issues/73485
    # In this case no validation is done
    static_argnums = () if static_argnums is None else _ensure_index_tuple(static_argnums)
    static_argnames = () if static_argnames is None else _ensure_str_tuple(static_argnames)
  else:
    # Infer argnums and argnames according to docstring
    static_argnums, static_argnames = _infer_argnums_and_argnames(
        sig, static_argnums, static_argnames)

    # Validation
    validate_argnums(sig, static_argnums, "static_argnums")
    validate_argnums(sig, donate_argnums, "donate_argnums")

    validate_argnames(sig, static_argnames, "static_argnames")

  # Compensate for static argnums absorbing args
  donate_argnums = rebase_donate_argnums(donate_argnums, static_argnums)

  if use_cpp_jit:
    return _cpp_jit(
        fun, static_argnums=static_argnums, static_argnames=static_argnames,
        device=device, backend=backend, donate_argnums=donate_argnums,
        inline=inline, keep_unused=keep_unused)

  return _python_jit(
      fun, static_argnums=static_argnums, static_argnames=static_argnames,
      device=device, backend=backend, donate_argnums=donate_argnums,
      inline=inline, keep_unused=keep_unused, abstracted_axes=abstracted_axes)
