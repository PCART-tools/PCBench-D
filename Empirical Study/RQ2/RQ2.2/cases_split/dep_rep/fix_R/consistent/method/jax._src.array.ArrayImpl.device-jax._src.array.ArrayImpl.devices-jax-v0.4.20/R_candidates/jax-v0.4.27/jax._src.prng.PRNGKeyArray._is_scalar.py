  def _is_scalar(self):
    base_ndim = len(self._impl.key_shape)
    return self._base_array.ndim == base_ndim
