def define(
    group_name,
    name,
    fun,
    arg_descriptors,
    *,
    dtype,
    rng_factory=jtu.rand_default,
    jax_unimplemented: Sequence[Limitation] = (),
    **params):
  """Defines a harness and stores it in `all_harnesses`. See Harness."""
  group_name = str(group_name)
  h = Harness(
      group_name,
      name,
      fun,
      arg_descriptors,
      rng_factory=rng_factory,
      jax_unimplemented=jax_unimplemented,
      dtype=dtype,
      **params)
  all_harnesses.append(h)
