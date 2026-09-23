def canonicalize_precision(precision: PrecisionLike) -> Optional[Tuple[PrecisionType, PrecisionType]]:
  """Turns an API precision specification, into a pair of enumeration values.

  The API can take the precision as a string, or int, and either as a single
  value to apply to both operands, or as a sequence of two values.
  """
  if precision is None:
    if config.jax_default_matmul_precision is None:
      return None
    try:
      return type_cast(
          Tuple[PrecisionType, PrecisionType],
          (Precision(config.jax_default_matmul_precision),
           Precision(config.jax_default_matmul_precision)))
    except TypeError:
      raise ValueError(
          "jax_default_matmul_precision flag must be set to None or a value in "
          f"{list(Precision._strings)}, but got {config.jax_default_matmul_precision}"
      ) from None
  elif isinstance(precision, str) and precision in Precision._strings:
    return type_cast(Tuple[PrecisionType, PrecisionType],
                     (Precision(precision), Precision(precision)))
  elif isinstance(precision, xla_client.PrecisionConfig.Precision):
    return type_cast(Tuple[PrecisionType, PrecisionType], (precision, precision))
  elif (isinstance(precision, (list, tuple)) and len(precision) == 2 and
        all(isinstance(p, xla_client.PrecisionConfig.Precision) for p in precision)):
    return type_cast(Tuple[PrecisionType, PrecisionType], precision)
  elif (isinstance(precision, (list, tuple)) and len(precision) == 2 and
        all(isinstance(s, str) for s in precision)):
    s1, s2 = precision
    p1 = type_cast(Tuple[PrecisionType, PrecisionType], canonicalize_precision(s1))[0]
    p2 = type_cast(Tuple[PrecisionType, PrecisionType], canonicalize_precision(s2))[0]
    return (p1, p2)
  else:
    raise ValueError(
        f"Precision argument must be None, a string in {list(Precision._strings)}, "
        "a lax.Precision value or a tuple of two lax.Precision values or "
        f"strings; got {precision}.")
