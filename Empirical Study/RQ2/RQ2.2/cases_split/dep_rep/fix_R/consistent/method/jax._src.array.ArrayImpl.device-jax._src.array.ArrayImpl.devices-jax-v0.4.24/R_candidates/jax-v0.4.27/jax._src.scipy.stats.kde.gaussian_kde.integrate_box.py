  def integrate_box(self, low_bounds, high_bounds, maxpts=None):
    """This method is not implemented in the JAX interface."""
    del low_bounds, high_bounds, maxpts
    raise NotImplementedError(
        "only 1D box integrations are supported; use `integrate_box_1d`")
