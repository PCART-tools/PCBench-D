@_wraps(np.moveaxis, lax_description=_ARRAY_VIEW_DOC)
def moveaxis(a, source: Union[int, Sequence[int]],
             destination: Union[int, Sequence[int]]):
  return _moveaxis(a, _ensure_index_tuple(source),
                   _ensure_index_tuple(destination))
