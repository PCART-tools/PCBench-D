  def evaluate(self, points):
    """Evaluate the Gaussian KDE on the given points."""
    check_arraylike("evaluate", points)
    points = self._reshape_points(points)
    result = _gaussian_kernel_eval(False, self.dataset.T, self.weights[:, None],
                                   points.T, self.inv_cov)
    return result[:, 0]
