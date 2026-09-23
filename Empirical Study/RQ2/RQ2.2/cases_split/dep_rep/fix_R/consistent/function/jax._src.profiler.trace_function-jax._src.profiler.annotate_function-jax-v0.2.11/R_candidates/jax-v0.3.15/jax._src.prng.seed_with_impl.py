def seed_with_impl(impl: PRNGImpl, seed: int) -> PRNGKeyArray:
  return PRNGKeyArray(impl, impl.seed(seed))
