def seed_with_impl(impl: PRNGImpl, seed: Union[int, Array]) -> PRNGKeyArray:
  return random_seed(seed, impl=impl)
