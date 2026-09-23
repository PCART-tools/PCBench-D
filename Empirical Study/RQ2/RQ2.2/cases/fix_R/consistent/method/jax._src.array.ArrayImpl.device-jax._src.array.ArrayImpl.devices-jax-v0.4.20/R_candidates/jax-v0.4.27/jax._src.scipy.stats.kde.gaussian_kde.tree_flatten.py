  def tree_flatten(self):
    return ((self.neff, self.dataset, self.weights, self.covariance,
             self.inv_cov), None)
