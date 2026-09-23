  def bind(self, fun, *args, in_axes, **params):
    assert len(in_axes) == len(args), (in_axes, args)
    return core.map_bind(self, fun, *args, in_axes=in_axes, **params)
