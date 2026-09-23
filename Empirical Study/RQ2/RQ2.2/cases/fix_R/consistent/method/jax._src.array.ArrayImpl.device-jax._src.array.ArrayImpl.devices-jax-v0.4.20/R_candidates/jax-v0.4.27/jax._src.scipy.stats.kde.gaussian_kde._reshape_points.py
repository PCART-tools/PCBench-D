  def _reshape_points(self, points):
    if jnp.issubdtype(lax.dtype(points), jnp.complexfloating):
      raise NotImplementedError(
          "gaussian_kde does not support complex coordinates")
    points = jnp.atleast_2d(points)
    d, m = points.shape
    if d != self.d:
      if d == 1 and m == self.d:
        points = jnp.reshape(points, (self.d, 1))
      else:
        raise ValueError(
            "points have dimension {}, dataset has dimension {}".format(
                d, self.d))
    return points
