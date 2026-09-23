  @property
  def sharding(self):
    # This attribute is part of the jax.Array API, but only defined on concrete arrays.
    # Raising a ConcretizationTypeError would make sense, but for backward compatibility
    # we raise an AttributeError so that hasattr() and getattr() work as expected.
    try:
      orig_msg = self._origin_msg()
    except:
      orig_msg = ''
    raise AttributeError(self,
      f"The 'sharding' attribute is not available on {self._error_repr()}."
      f"{orig_msg}")
