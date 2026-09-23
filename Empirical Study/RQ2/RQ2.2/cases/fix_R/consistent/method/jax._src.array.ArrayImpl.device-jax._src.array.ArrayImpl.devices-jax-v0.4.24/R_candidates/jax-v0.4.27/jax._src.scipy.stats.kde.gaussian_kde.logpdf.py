  def logpdf(self, x):
    """Log probability density function"""
    check_arraylike("logpdf", x)
    x = self._reshape_points(x)
    result = _gaussian_kernel_eval(True, self.dataset.T, self.weights[:, None],
                                   x.T, self.inv_cov)
    return result[:, 0]
