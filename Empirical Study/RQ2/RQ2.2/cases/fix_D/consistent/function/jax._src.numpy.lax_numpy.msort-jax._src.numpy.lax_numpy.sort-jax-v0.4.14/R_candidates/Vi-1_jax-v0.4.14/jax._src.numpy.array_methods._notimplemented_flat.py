def _notimplemented_flat(self):
  raise NotImplementedError("JAX DeviceArrays do not implement the arr.flat property: "
                            "consider arr.flatten() instead.")
