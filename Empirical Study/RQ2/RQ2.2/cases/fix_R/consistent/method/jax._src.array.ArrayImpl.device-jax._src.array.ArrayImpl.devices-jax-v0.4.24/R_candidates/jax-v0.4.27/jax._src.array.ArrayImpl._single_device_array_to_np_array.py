  @use_cpp_method()
  def _single_device_array_to_np_array(self):
    return np.asarray(self._arrays[0])
