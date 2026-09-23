def _flatten_defaultdict(d):
  keys = tuple(sorted(d))
  return tuple(d[k] for k in keys), (d.default_factory, keys)
