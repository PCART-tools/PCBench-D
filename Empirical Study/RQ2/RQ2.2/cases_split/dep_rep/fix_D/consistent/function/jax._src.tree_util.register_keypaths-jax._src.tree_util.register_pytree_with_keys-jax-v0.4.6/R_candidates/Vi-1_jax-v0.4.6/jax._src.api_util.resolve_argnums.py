def resolve_argnums(
    fun, donate_argnums, static_argnums, static_argnames
) -> Tuple[Tuple[int, ...], Tuple[int, ...], Tuple[str, ...]]:
  # Coerce input
  donate_argnums = _ensure_index_tuple(donate_argnums)

  try:
    sig = inspect.signature(fun)
  except ValueError:
    # Some built-in functions don't support signature.
    # See: https://github.com/python/cpython/issues/73485
    # In this case no validation is done
    static_argnums = () if static_argnums is None else _ensure_index_tuple(
        static_argnums)
    static_argnames = () if static_argnames is None else _ensure_str_tuple(
        static_argnames)
  else:
    # Infer argnums and argnames according to docstring
    static_argnums, static_argnames = infer_argnums_and_argnames(
        sig, static_argnums, static_argnames)

    # Validation
    validate_argnums(sig, static_argnums, "static_argnums")
    validate_argnums(sig, donate_argnums, "donate_argnums")
    validate_argnames(sig, static_argnames, "static_argnames")

  # Compensate for static argnums absorbing args
  donate_argnums = rebase_donate_argnums(donate_argnums, static_argnums)
  return donate_argnums, static_argnums, static_argnames
