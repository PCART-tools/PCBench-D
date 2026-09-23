class RandArg(NamedTuple):
  """Descriptor for a randomly generated argument.

  See description of `Harness`.
  """
  shape: tuple[int, ...]
  dtype: DType
