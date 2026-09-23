def eye(N, chunks, M=None, k=0, dtype=float):
    """
    Return a 2-D Array with ones on the diagonal and zeros elsewhere.

    Parameters
    ----------
    N : int
      Number of rows in the output.
    chunks: int
        chunk size of resulting blocks
    M : int, optional
      Number of columns in the output. If None, defaults to `N`.
    k : int, optional
      Index of the diagonal: 0 (the default) refers to the main diagonal,
      a positive value refers to an upper diagonal, and a negative value
      to a lower diagonal.
    dtype : data-type, optional
      Data-type of the returned array.

    Returns
    -------
    I : Array of shape (N,M)
      An array where all elements are equal to zero, except for the `k`-th
      diagonal, whose values are equal to one.
    """
    if not isinstance(chunks, int):
        raise ValueError('chunks must be an int')

    token = tokenize(N, chunk, M, k, dtype)
    name_eye = 'eye-' + token

    eye = {}
    if M is None:
        M = N

    vchunks = [chunks] * (N // chunks)
    if N % chunks != 0:
        vchunks.append(N % chunks)
    hchunks = [chunks] * (M // chunks)
    if M % chunks != 0:
        hchunks.append(M % chunks)

    for i, vchunk in enumerate(vchunks):
        for j, hchunk in enumerate(hchunks):
            if (j - i - 1) * chunks <= k <= (j - i + 1) * chunks:
                eye[name_eye, i, j] = (np.eye, vchunk, hchunk, k - (j - i) * chunks, dtype)
            else:
                eye[name_eye, i, j] = (np.zeros, (vchunk, hchunk), dtype)
    return Array(eye, name_eye, shape=(N, M),
                 chunks=(chunks, chunks), dtype=dtype)
