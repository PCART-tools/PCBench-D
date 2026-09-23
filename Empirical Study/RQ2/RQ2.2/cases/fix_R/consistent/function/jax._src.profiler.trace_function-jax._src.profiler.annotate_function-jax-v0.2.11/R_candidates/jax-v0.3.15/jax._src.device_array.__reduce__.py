  def __reduce__(self):
    fun, args, arr_state = self._value.__reduce__()
    aval_state = {'weak_type': self.aval.weak_type,
                  'named_shape': self.aval.named_shape}
    return (reconstruct_device_array, (fun, args, arr_state, aval_state))
