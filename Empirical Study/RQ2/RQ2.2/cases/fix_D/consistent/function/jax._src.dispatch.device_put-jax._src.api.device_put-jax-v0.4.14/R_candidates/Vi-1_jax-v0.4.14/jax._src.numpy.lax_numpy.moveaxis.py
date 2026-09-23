@util._wraps(np.moveaxis, lax_description=_ARRAY_VIEW_DOC)
def moveaxis(a: ArrayLike, source: Union[int, Sequence[int]],
             destination: Union[int, Sequence[int]]) -> Array:
  util.check_arraylike("moveaxis", a)
  return _moveaxis(asarray(a), _ensure_index_tuple(source),
                   _ensure_index_tuple(destination))
