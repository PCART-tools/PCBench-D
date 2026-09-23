def register_translation(prim: core.Primitive, rule: TranslationRule, *,
                         platform: str | None = None) -> None:
  if platform is None:
    _translations[prim] = rule
  else:
    # For backward compatibility reasons, we allow rules to be registered
    # under "gpu" even though the platforms are now called "cuda" and "rocm".
    # TODO(phawkins): fix up users to specify either "cuda" or "rocm" and remove
    # this expansion.
    for p in xb.expand_platform_alias(platform):
      _backend_specific_translations[p][prim] = rule
