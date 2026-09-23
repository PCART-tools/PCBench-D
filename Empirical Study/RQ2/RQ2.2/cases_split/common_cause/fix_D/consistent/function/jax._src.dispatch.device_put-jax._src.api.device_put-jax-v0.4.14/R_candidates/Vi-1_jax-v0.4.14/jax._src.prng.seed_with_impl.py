def seed_with_impl(impl: PRNGImpl, seed: int | Array) -> PRNGKeyArrayImpl:
  return random_seed(seed, impl=impl)
