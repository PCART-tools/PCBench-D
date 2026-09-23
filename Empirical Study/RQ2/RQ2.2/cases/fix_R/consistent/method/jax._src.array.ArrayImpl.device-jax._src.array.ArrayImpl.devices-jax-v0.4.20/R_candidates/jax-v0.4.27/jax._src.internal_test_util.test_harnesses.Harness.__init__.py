  def __init__(self,
               group_name,
               name,
               fun,
               arg_descriptors,
               *,
               dtype,
               rng_factory=jtu.rand_default,
               jax_unimplemented: Sequence[Limitation] = (),
               **params):
    """See class docstring."""
    self.group_name = jtu.sanitize_test_name(group_name)
    self.name = jtu.sanitize_test_name(name)
    self.fullname = self.name if self.group_name is None else f"{self.group_name}_{self.name}"
    self.fun = fun  # type: ignore[assignment]
    self.arg_descriptors = arg_descriptors
    self.rng_factory = rng_factory  # type: ignore[assignment]
    self.jax_unimplemented = jax_unimplemented
    self.dtype = dtype
    self.params = params
