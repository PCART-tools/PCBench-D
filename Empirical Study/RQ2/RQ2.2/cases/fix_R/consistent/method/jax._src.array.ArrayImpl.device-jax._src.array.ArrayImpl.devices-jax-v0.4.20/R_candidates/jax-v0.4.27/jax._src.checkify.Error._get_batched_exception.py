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
