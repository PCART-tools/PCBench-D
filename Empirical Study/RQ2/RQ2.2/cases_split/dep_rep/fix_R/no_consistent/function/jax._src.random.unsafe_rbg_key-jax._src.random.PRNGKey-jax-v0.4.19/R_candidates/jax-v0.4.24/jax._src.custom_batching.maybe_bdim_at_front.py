def maybe_bdim_at_front(x, bdim):
  if bdim is not_mapped:
    return x
  else:
    return util.moveaxis(x, bdim, 0)
