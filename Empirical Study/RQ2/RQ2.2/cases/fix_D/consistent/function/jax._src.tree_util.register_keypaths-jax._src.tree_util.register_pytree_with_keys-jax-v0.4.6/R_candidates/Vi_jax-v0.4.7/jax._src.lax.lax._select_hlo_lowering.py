def _select_hlo_lowering(ctx, which, *cases):
  which_aval = ctx.avals_in[0]
  if which_aval.dtype == np.dtype(np.bool_):
    assert len(cases) <= 2
    if len(cases) == 1: return cases
    return hlo.SelectOp(which, cases[1], cases[0]).results

  if dtypes.issubdtype(which_aval.dtype, np.signedinteger):
    compare_type = 'SIGNED'
  else:
    compare_type = 'UNSIGNED'
  lt = 'LT'

  def _select(offset, cases):
    assert len(cases) > 0
    if len(cases) == 1:
      return cases[0]
    mid = len(cases) // 2
    pred = mlir.compare_hlo(which,
                            mlir.full_like_aval(ctx, offset + mid, which_aval),
                            lt, compare_type)
    return hlo.SelectOp(pred, _select(offset, cases[:mid]),
                        _select(offset + mid, cases[mid:])).result

  return [_select(0, cases)]
