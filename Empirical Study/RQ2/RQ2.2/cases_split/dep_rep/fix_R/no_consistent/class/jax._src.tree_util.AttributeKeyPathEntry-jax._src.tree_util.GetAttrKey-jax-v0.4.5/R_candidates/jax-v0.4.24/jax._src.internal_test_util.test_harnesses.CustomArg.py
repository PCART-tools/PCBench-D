class CustomArg(NamedTuple):
  """Descriptor for a dynamic argument generated from a PRNG factory.

  See description of `Harness`.
  """
  make: Callable[[Rng], Any]  # Called with a Rng to make a tensor
