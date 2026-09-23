  @classmethod
  def tree_unflatten(cls, aux_data, children):
    del aux_data
    kde = cls.__new__(cls)
    kde._setattr("neff", children[0])
    kde._setattr("dataset", children[1])
    kde._setattr("weights", children[2])
    kde._setattr("covariance", children[3])
    kde._setattr("inv_cov", children[4])
    return kde
