def seed_with_impl(impl: PRNGImpl, seed: int) -> PRNGKeyArray:
  return random_seed(seed, impl=impl)
