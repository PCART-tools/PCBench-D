class JitWrapped(stages.Wrapped):

  def eval_shape(self, *args, **kwargs):
    """See ``jax.eval_shape``."""
    raise NotImplementedError
