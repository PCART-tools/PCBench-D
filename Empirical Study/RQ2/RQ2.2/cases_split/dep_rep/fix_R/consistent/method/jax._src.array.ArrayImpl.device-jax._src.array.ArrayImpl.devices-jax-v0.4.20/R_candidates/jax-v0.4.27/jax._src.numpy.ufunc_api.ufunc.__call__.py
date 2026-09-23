  def __call__(self, *args: ArrayLike,
               out: None = None, where: None = None,
               **kwargs: Any) -> Any:
    if out is not None:
      raise NotImplementedError(f"out argument of {self}")
    if where is not None:
      raise NotImplementedError(f"where argument of {self}")
    return self._call(*args, **kwargs)
