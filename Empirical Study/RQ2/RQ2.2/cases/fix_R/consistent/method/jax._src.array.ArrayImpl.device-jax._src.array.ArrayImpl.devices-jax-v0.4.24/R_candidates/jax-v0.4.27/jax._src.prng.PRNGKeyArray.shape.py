  @property
  def shape(self):
    return base_arr_shape_to_keys_shape(self._impl, self._base_array.shape)
