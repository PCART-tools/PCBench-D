def _select_transpose_rule(t, which, *cases):
  assert not ad.is_undefined_primal(which)
  if type(t) is ad_util.Zero:
    return [None] + [ad_util.Zero(c.aval) if ad.is_undefined_primal(c) else None
                     for c in cases]
  else:
    zeros = full_like(t, 0)
    return [None] + [
        select(eq(which, _const(which, i)), t, zeros)
        if ad.is_undefined_primal(case) else None
        for i, case in enumerate(cases)
    ]
