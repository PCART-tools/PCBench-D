def _concatenate_pad_rule(in_avals, out_avals, *operands, dimension):
  if all(isinstance(a.shape[dimension], (int, np.integer))
         for a in in_avals):
    return [concatenate(operands, dimension)]
  else:
    raise NotImplementedError  # TODO(mattjj)
