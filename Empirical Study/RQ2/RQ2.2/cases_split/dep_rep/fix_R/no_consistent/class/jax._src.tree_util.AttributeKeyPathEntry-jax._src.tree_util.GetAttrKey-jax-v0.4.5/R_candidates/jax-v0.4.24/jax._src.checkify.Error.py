@jtu.register_pytree_node_class
@dataclasses.dataclass(frozen=True)
class Error:
  _pred: dict[ErrorEffect, Bool]
  _code: dict[ErrorEffect, Int]
  _metadata: dict[Int, PyTreeDef]  # mapping of code to JaxException treedef.
  _payload: dict[ErrorEffect, Payload]

  def get(self) -> str | None:
    """Returns error message if error happened, None if no error happened."""
    exp = self.get_exception()
    if exp is not None:
      return str(exp)
    return None

  def get_exception(self) -> JaxException | None:
    """Returns Python exception if error happened, None if no error happened."""
    if any(map(np.shape, self._pred.values())):
      return self._get_batched_exception()
    else:
      min_code = None
      cur_effect = None
      for error_effect, code in self._code.items():
        if self._pred[error_effect]:
          if min_code is None or code < min_code:
            min_code = code
            cur_effect = error_effect

      if cur_effect is not None:
        return tree_unflatten(self._metadata[int(min_code)],  # type: ignore
                              self._payload[cur_effect])
    return None

  def throw(self):
    _check_error(self)

  def __str__(self):
    return f'Error({self.get()})'

  # Internal helpers

  def _get_batched_exception(self) -> BatchedError | None:
    shape = np.shape(list(self._pred.values())[0])
    error_mapping = {}
    for idx in np.ndindex(*shape):
      min_code = None
      cur_effect = None
      for error_effect, code in self._code.items():
        if self._pred[error_effect][idx]:   # type: ignore
          if min_code is None or code[idx] < min_code:
            min_code = code[idx]   # type: ignore
            cur_effect = error_effect

      if cur_effect is not None:
        payload = tree_map(lambda x, i=idx: x[i], self._payload[cur_effect])
        jax_error = tree_unflatten(self._metadata[int(min_code)], payload)  # type: ignore
        error_mapping[idx] = jax_error
    if error_mapping:
      return BatchedError(error_mapping)
    else:
      return None

  def _update(self, effect_type: ErrorEffect, pred, code, metadata, payload):
    new_errs = {**self._pred, **{effect_type: pred}}  # type: ignore
    new_codes = {**self._code, **{effect_type: code}}  # type: ignore
    new_payload = {**self._payload, **{effect_type: payload}}  # type: ignore
    new_metadata = {**self._metadata, **metadata}
    return Error(new_errs, new_codes, new_metadata, new_payload)

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

  def _replace(self, *args, **kwargs):
    return dataclasses.replace(self, *args, **kwargs)

  # PyTree methods

  def tree_flatten(self):
    return ((self._pred, self._code, self._payload), (self._metadata))

  @classmethod
  def tree_unflatten(cls, metadata, data):
    pred, code, payload = data
    return cls(pred, code, metadata, payload)
