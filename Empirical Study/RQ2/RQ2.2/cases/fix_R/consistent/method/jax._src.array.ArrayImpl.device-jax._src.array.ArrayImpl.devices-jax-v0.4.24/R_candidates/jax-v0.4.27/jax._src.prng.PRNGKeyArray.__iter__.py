  def __iter__(self) -> Iterator[PRNGKeyArray]:
    if self._is_scalar():
      raise TypeError('iteration over a 0-d key array')
    # TODO(frostig): we may want to avoid iteration by slicing because
    # a very common use of iteration is `k1, k2 = split(key)`, and
    # slicing/indexing may be trickier to track for linearity checking
    # purposes. Maybe we can:
    # * introduce an unpack primitive+traceable (also allow direct use)
    # * unpack upfront into shape[0] many keyarray slices
    # * return iter over these unpacked slices
    # Whatever we do, we'll want to do it by overriding
    # ShapedArray._iter when the element type is KeyTy...
    return (PRNGKeyArray(self._impl, k) for k in iter(self._base_array))
