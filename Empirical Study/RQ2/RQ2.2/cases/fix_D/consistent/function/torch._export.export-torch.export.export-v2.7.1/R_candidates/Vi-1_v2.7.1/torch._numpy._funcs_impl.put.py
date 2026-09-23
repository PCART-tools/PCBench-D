def put(
    a: NDArray,
    indices: ArrayLike,
    values: ArrayLike,
    mode: NotImplementedType = "raise",
):
    v = values.type(a.dtype)
    # If indices is larger than v, expand v to at least the size of indices. Any
    # unnecessary trailing elements are then trimmed.
    if indices.numel() > v.numel():
        ratio = (indices.numel() + v.numel() - 1) // v.numel()
        v = v.unsqueeze(0).expand((ratio,) + v.shape)
    # Trim unnecessary elements, regardless if v was expanded or not. Note
    # np.put() trims v to match indices by default too.
    if indices.numel() < v.numel():
        v = v.flatten()
        v = v[: indices.numel()]
    a.put_(indices, v)
    return None
