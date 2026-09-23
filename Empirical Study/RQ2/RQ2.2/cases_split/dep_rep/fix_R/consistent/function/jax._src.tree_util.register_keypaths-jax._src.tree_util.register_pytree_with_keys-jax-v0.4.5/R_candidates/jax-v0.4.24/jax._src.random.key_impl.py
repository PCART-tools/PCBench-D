def key_impl(keys: KeyArrayLike) -> Hashable:
  typed_keys, _ = _check_prng_key("key_impl", keys, allow_batched=True)
  return PRNGSpec(_key_impl(typed_keys))
