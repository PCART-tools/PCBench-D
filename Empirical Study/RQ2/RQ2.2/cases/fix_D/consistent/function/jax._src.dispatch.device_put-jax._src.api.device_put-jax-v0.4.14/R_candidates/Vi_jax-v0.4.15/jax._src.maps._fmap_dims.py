def _fmap_dims(axes, f):
  return AxisNamePos(((name, f(axis)) for name, axis in axes.items()),
                     user_repr=axes.user_repr)
