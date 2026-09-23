  def _add_placeholder_effects(self, effects: set[ErrorEffect]):
    """Fill out Error with `effects` and np.ones arrays of their payloads."""
    new_err = self._pred.copy()
    new_code = self._code.copy()
    new_payload = self._payload.copy()
    for effect in effects:
      if effect not in self._pred.keys():
        new_err[effect] = False
        new_payload[effect] = list(
            tree_map(lambda a: jnp.ones(a.shape, a.dtype), effect.shape_dtypes))
        # The error value associated with this effect will never become True, so
        # we don't need to set a meaningful code.
        new_code[effect] = -1
    return Error(new_err, new_code, self._metadata, new_payload)
