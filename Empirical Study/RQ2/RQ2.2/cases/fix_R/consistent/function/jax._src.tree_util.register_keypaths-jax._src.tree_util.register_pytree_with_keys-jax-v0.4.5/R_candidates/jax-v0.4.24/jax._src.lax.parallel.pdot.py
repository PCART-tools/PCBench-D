def pdot(x, y, axis_name, pos_contract=((), ()), pos_batch=((), ()),
         precision=None):
  if not isinstance(axis_name, (list, tuple)):
    axis_name = (axis_name,)
  pos_contract = tuple(map(tuple, pos_contract))
  pos_batch = tuple(map(tuple, pos_batch))
  return pdot_p.bind(x, y, axis_name=tuple(axis_name),
                     pos_contract=pos_contract, pos_batch=pos_batch,
                     precision=lax.canonicalize_precision(precision))
