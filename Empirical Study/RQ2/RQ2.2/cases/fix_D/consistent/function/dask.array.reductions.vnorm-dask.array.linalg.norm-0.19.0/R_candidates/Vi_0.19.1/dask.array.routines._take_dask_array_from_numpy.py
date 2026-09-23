def _take_dask_array_from_numpy(a, indices, axis):
    assert isinstance(a, np.ndarray)
    assert isinstance(indices, Array)

    return indices.map_blocks(lambda block: np.take(a, block, axis),
                              chunks=indices.chunks,
                              dtype=a.dtype)
