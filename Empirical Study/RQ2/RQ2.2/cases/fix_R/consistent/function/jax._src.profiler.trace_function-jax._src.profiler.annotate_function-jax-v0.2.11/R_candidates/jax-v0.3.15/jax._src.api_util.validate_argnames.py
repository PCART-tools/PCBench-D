def validate_argnames(sig: inspect.Signature, argnames: Tuple[str, ...], argnames_name: str) -> None:
  """
  Validate that the argnames are sensible for a given function.

  For functions that accept a variable keyword arguments
  (`f(..., **kwargs)`) all argnames are considered valid except those
  marked as position-only (`f(pos_only, /, ...)`).
  """
  var_kwargs = False
  valid_kwargs: Set[str] = set()
  invalid_kwargs: Set[str] = set()
  for param_name, param in sig.parameters.items():
    if param.kind in _KEYWORD_ARGUMENTS:
      valid_kwargs.add(param_name)

    elif param.kind is inspect.Parameter.VAR_KEYWORD:
      var_kwargs = True

    elif param.kind in _INVALID_KEYWORD_ARGUMENTS:
      invalid_kwargs.add(param_name)


  # Check whether any kwargs are invalid due to position only
  invalid_argnames = invalid_kwargs & set(argnames)
  if invalid_argnames:
    # raise ValueError(f"Jitted function has invalid argnames {invalid_argnames} "
    #                  f"in {argnames_name}. These are positional-only")
    # TODO: 2022-08-20 or later: replace with error
    warnings.warn(f"Jitted function has invalid argnames {invalid_argnames} "
                  f"in {argnames_name}. These are positional-only. "
                  "This warning will be replaced by an error after 2022-08-20 "
                  "at the earliest.", SyntaxWarning)

  # Takes any kwargs
  if var_kwargs:
    return

  # Check that all argnames exist on function
  invalid_argnames = set(argnames) - valid_kwargs
  if invalid_argnames:
    # TODO: 2022-08-20 or later: replace with error
    # raise ValueError(f"Jitted function has invalid argnames {invalid_argnames} "
    #                  f"in {argnames_name}. Function does not take these args.")
    warnings.warn(f"Jitted function has invalid argnames {invalid_argnames} "
                  f"in {argnames_name}. Function does not take these args."
                  "This warning will be replaced by an error after 2022-08-20 "
                  "at the earliest.", SyntaxWarning)
