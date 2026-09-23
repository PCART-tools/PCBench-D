def segment_ids(size, is_sorted):
    if size == 0:
        return st.just(np.empty(shape=[0], dtype=np.int32))
    if is_sorted:
        return arrays(
            [size],
            dtype=np.int32,
            elements=st.booleans()).map(
                lambda x: np.cumsum(x, dtype=np.int32) - x[0])
    else:
        return arrays(
            [size],
            dtype=np.int32,
            elements=st.integers(min_value=0, max_value=2 * size))
