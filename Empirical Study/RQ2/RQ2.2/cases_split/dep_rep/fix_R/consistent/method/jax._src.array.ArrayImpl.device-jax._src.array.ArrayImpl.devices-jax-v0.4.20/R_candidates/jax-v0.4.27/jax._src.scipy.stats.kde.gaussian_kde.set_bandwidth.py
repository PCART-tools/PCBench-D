  def set_bandwidth(self, bw_method=None):
    """This method is not implemented in the JAX interface."""
    del bw_method
    raise NotImplementedError(
        "dynamically changing the bandwidth method is not supported")
