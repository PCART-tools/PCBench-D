  def wrap(self, gen, gen_static_args, out_store) -> WrappedFun:
    """Add another transform and its store."""
    return WrappedFun(self.f, ((gen, gen_static_args),) + self.transforms,
                      (out_store,) + self.stores, self.params, None, None)
