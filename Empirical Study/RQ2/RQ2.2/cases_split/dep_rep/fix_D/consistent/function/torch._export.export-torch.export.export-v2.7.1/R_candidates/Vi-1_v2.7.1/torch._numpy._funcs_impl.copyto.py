def copyto(
    dst: NDArray,
    src: ArrayLike,
    casting: Optional[CastingModes] = "same_kind",
    where: NotImplementedType = None,
):
    (src,) = _util.typecast_tensors((src,), dst.dtype, casting=casting)
    dst.copy_(src)
