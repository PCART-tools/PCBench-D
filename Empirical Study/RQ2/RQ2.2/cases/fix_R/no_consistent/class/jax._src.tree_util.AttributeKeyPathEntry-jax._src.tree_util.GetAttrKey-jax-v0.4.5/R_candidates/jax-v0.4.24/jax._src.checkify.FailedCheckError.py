class FailedCheckError(JaxException):

  def __init__(self, traceback_info, fmt_string, *a, **k):
    super().__init__(traceback_info)
    self.fmt_string = fmt_string
    self.args = a
    self.kwargs = k

  def tree_flatten(self):
    return ((self.args, self.kwargs),  # leaves
            (self.traceback_info, self.fmt_string))  # treedef

  @classmethod
  def tree_unflatten(cls, metadata, payload):
    args, kwargs = payload
    return cls(*metadata, *args, **kwargs)

  def __str__(self):
    return (self.fmt_string.format(*self.args, **self.kwargs)
            + ' (`check` failed)')

  def get_effect_type(self):
    vals = jtu.tree_leaves((self.args, self.kwargs))
    return ErrorEffect(
        FailedCheckError,
        tuple(api.ShapeDtypeStruct(x.shape, x.dtype) for x in vals))
