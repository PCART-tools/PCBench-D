def lengths(size, min_segments=None, max_segments=None, **kwargs):
    # First generate number of boarders between segments
    # Then create boarder values and add 0 and size
    # By sorting and computing diff we convert them to lengths of
    # possible 0 value
    if min_segments is None:
        min_segments = 0
    if max_segments is None:
        max_segments = size
    assert min_segments >= 0
    assert min_segments <= max_segments
    if size == 0 and max_segments == 0:
        return st.just(np.empty(shape=[0], dtype=np.int32))
    assert max_segments > 0, "size is not 0, need at least one segment"
    return st.integers(
        min_value=max(min_segments - 1, 0), max_value=max_segments - 1
    ).flatmap(
        lambda num_borders:
        hypothesis.extra.numpy.arrays(
            np.int32, num_borders, elements=st.integers(
                min_value=0, max_value=size
            )
        )
    ).map(
        lambda x: np.append(x, np.array([0, size], dtype=np.int32))
    ).map(sorted).map(np.diff)
