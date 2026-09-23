@util._wraps(np.array_split)
def array_split(ary: ArrayLike, indices_or_sections: Union[int, ArrayLike], axis: int = 0) -> List[Array]:
  return _split("array_split", ary, indices_or_sections, axis=axis)
