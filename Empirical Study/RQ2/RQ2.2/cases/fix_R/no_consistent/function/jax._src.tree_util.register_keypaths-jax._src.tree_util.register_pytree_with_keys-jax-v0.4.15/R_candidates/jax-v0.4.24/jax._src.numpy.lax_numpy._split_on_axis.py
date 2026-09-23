def _split_on_axis(op: str, axis: int) -> Callable[[ArrayLike, int | ArrayLike], list[Array]]:
  @util.implements(getattr(np, op), update_doc=False)
  def f(ary: ArrayLike, indices_or_sections: int | Sequence[int] | ArrayLike) -> list[Array]:
    # for 1-D array, hsplit becomes vsplit
    nonlocal axis
    util.check_arraylike(op, ary)
    a = asarray(ary)
    if axis == 1 and len(a.shape) == 1:
      axis = 0
    return _split(op, ary, indices_or_sections, axis=axis)
  return f
