@util.implements(np.array_split)
def array_split(ary: ArrayLike, indices_or_sections: int | Sequence[int] | ArrayLike,
                axis: int = 0) -> list[Array]:
  return _split("array_split", ary, indices_or_sections, axis=axis)
