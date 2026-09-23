  def bind(self, fun, *args, **params):
    assert len(params['in_axes']) == len(args)
    return map_bind(self, fun, *args, **params)
