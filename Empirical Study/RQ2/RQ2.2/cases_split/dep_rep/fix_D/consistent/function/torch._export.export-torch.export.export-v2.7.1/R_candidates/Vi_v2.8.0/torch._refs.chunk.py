def chunk(a: TensorLikeType, chunks: int, dim: int = 0) -> tuple[TensorLikeType, ...]:
    if chunks <= 0:
        msg = f"Expected at least one chunk, but got {chunks}!"
        raise ValueError(msg)

    dim = utils.canonicalize_dim(a.ndim, dim)
    length = a.shape[dim]
    chunk_size = math.ceil(length / chunks)
    full_chunks = math.floor(length / chunk_size)
    tail_chunk_size = length % chunk_size

    result = [narrow(a, dim, i * chunk_size, chunk_size) for i in range(full_chunks)]

    if tail_chunk_size != 0:
        result.append(narrow(a, dim, full_chunks * chunk_size, tail_chunk_size))

    return tuple(result)
