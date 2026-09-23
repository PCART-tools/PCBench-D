def resolve_prng_impl(impl_spec: Optional[str]):
  if impl_spec is None:
    return default_prng_impl()
  if impl_spec in PRNG_IMPLS:
    return PRNG_IMPLS[impl_spec]

  keys_fmt = ', '.join(f'"{s}"' for s in PRNG_IMPLS.keys())
  raise ValueError(f'unrecognized PRNG implementation "{impl_spec}". '
                   f'Did you mean one of: {keys_fmt}?')
