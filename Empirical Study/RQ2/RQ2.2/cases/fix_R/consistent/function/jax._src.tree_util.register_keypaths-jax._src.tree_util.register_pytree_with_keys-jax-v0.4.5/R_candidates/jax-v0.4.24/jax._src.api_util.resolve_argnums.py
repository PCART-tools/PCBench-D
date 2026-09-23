def resolve_argnums(
    fun, donate_argnums, donate_argnames, static_argnums, static_argnames
) -> tuple[tuple[int, ...], tuple[str, ...], tuple[int, ...], tuple[str, ...]]:
  try:
    sig = inspect.signature(fun)
  except ValueError as e:
    # Some built-in functions don't support signature.
    # See: https://github.com/python/cpython/issues/73485
    # In this case no validation is done
    static_argnums = () if static_argnums is None else _ensure_index_tuple(
        static_argnums)
    static_argnames = () if static_argnames is None else _ensure_str_tuple(
        static_argnames)
    donate_argnums = () if donate_argnums is None else _ensure_index_tuple(
        donate_argnums)
    if donate_argnames is not None:
      raise ValueError(f"Getting the signature of function {fun} failed. "
                       "Pass donate_argnums instead of donate_argnames.") from e
    assert donate_argnames is None
    donate_argnames = ()
  else:
    # Infer argnums and argnames according to docstring
    # If nums is None and names is not None, then nums are inferred from the
    # names and vice-versa.
    static_argnums, static_argnames = infer_argnums_and_argnames(
        sig, static_argnums, static_argnames)
    donate_argnums, donate_argnames = infer_argnums_and_argnames(
        sig, donate_argnums, donate_argnames)

    # Validation
    validate_argnums(sig, static_argnums, "static_argnums")
    validate_argnames(sig, static_argnames, "static_argnames")
    validate_argnums(sig, donate_argnums, "donate_argnums")
    validate_argnames(sig, donate_argnames, "donate_argnames")

  # Compensate for static argnums absorbing args
  assert_no_intersection(static_argnames, donate_argnames)
  donate_argnums = rebase_donate_argnums(donate_argnums, static_argnums)
  return donate_argnums, donate_argnames, static_argnums, static_argnames
