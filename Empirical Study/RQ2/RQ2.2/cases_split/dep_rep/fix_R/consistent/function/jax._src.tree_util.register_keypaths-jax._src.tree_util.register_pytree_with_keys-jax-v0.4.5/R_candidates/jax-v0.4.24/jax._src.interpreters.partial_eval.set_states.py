def set_states(attrs_tracked: AttrsTracked, vals: AttrStates):
  for ((obj, attr), val) in zip(attrs_tracked, vals):
    setattr(obj, attr, val)
