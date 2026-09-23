def _split_on_axis(op: str, axis: int) -> Callable[[ArrayLike, Union[int, ArrayLike]], List[Array]]:
  @util._wraps(getattr(np, op), update_doc=False)
  def f(ary: ArrayLike, indices_or_sections: Union[int, ArrayLike]) -> List[Array]:
    # for 1-D array, hsplit becomes vsplit
    nonlocal axis
    util._check_arraylike(op, ary)
    a = asarray(ary)
    if axis == 1 and len(a.shape) == 1:
      axis = 0
    return _split(op, ary, indices_or_sections, axis=axis)
  return f
