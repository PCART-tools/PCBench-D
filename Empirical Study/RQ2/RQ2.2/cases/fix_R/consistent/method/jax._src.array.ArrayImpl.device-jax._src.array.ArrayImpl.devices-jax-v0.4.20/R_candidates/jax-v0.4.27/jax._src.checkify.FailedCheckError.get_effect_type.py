  def get_effect_type(self):
    vals = jtu.tree_leaves((self.args, self.kwargs))
    return ErrorEffect(
        FailedCheckError,
        tuple(api.ShapeDtypeStruct(x.shape, x.dtype) for x in vals))
