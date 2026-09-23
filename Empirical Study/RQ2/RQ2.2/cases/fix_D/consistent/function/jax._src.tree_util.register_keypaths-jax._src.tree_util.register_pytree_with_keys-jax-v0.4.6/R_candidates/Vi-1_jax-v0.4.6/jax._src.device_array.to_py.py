  def to_py(self):
    warnings.warn("The .to_py() method on JAX arrays is deprecated. Use "
                  "np.asarray(...) instead.", category=FutureWarning)
    return np.asarray(self._value)
