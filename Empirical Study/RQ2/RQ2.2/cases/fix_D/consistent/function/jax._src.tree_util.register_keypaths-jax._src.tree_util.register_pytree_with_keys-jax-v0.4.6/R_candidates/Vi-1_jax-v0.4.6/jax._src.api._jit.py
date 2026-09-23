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
  check_callable(fun)

  donate_argnums, static_argnums, static_argnames = resolve_argnums(
      fun, donate_argnums, static_argnums, static_argnames)

  if use_cpp_jit:
    return _cpp_jit(
        fun, static_argnums=static_argnums, static_argnames=static_argnames,
        device=device, backend=backend, donate_argnums=donate_argnums,
        inline=inline, keep_unused=keep_unused)

  return _python_jit(
      fun, static_argnums=static_argnums, static_argnames=static_argnames,
      device=device, backend=backend, donate_argnums=donate_argnums,
      inline=inline, keep_unused=keep_unused, abstracted_axes=abstracted_axes)
