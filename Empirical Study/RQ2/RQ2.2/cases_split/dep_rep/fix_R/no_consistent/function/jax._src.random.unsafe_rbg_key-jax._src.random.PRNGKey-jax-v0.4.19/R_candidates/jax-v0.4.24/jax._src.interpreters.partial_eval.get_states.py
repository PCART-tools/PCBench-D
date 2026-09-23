def get_states(attrs_tracked: AttrsTracked):
  return [getattr(obj, attr) for (obj, attr) in attrs_tracked]
