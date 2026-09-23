  @use_cpp_method()
  def unsafe_buffer_pointer(self):
    if len(self._arrays) != 1:
      raise ValueError("unsafe_buffer_pointer() is supported only for unsharded"
                       " arrays.")
    return self._arrays[0].unsafe_buffer_pointer()
