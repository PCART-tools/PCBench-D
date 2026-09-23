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
