  def __init__(self, impl, key_data: Any):
    assert not isinstance(key_data, core.Tracer)
    _check_prng_key_data(impl, key_data)
    self._impl = impl
    self._base_array = key_data
    self._consumed = False  # TODO(jakevdp): default to True here?
