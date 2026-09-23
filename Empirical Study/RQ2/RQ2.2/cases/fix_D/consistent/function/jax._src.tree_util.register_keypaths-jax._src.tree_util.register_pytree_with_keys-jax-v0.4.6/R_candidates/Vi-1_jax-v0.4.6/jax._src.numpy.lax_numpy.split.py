@util._wraps(np.split, lax_description=_ARRAY_VIEW_DOC)
def split(ary: ArrayLike, indices_or_sections: Union[int, ArrayLike], axis: int = 0) -> List[Array]:
  return _split("split", ary, indices_or_sections, axis=axis)
