def validate_argnums(sig: inspect.Signature, argnums: tuple[int, ...], argnums_name: str) -> None:
  """
  Validate that the argnums are sensible for a given function.

  For functions that accept a variable number of positions arguments
  (`f(..., *args)`) all positive argnums are considered valid.
  """
  n_pos_args = 0
  for param in sig.parameters.values():
    if param.kind in _POSITIONAL_ARGUMENTS:
      n_pos_args += 1

    elif param.kind is inspect.Parameter.VAR_POSITIONAL:
      # We can have any number of positional arguments
      return

  if argnums and (-min(argnums) > n_pos_args or max(argnums) >= n_pos_args):
    # raise ValueError(f"Jitted function has {argnums_name}={argnums}, "
    #                  f"but only accepts {n_pos_args} positional arguments.")
    # TODO: 2022-08-20 or later: replace with error
    warnings.warn(f"Jitted function has {argnums_name}={argnums}, "
                  f"but only accepts {n_pos_args} positional arguments. "
                  "This warning will be replaced by an error after 2022-08-20 "
                  "at the earliest.", SyntaxWarning)
