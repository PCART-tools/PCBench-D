def _reducer_padding(traceable, ident, in_avals, out_avals, operand, *, axes):
  del out_avals
  aval, = in_avals
  padded_axes = [(i, d.val) for i, d in enumerate(aval.shape)
                 if isinstance(d, pe.BoundedAxisSize)]
  operand_ = _replace_masked_values(operand, ident(aval.dtype), padded_axes)
  return [traceable(operand_, axes)]
