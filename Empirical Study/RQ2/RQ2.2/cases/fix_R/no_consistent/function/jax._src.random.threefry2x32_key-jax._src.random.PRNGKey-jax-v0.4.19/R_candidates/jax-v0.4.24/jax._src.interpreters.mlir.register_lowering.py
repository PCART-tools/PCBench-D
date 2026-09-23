def register_lowering(prim: core.Primitive, rule: LoweringRule,
                      platform: str | None = None):
  if platform is None:
    _lowerings[prim] = rule
  else:
    # For backward compatibility reasons, we allow rules to be registered
    # under "gpu" even though the platforms are now called "cuda" and "rocm".
    # TODO(phawkins): fix up users to specify either "cuda" or "rocm" and remove
    # this expansion.
    for p in xb.expand_platform_alias(platform):
      _platform_specific_lowerings[p][prim] = rule
  return rule
