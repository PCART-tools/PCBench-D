@wraps(np.tile)
def tile(A, reps):
    if not isinstance(reps, Integral):
        raise NotImplementedError("Only integer valued `reps` supported.")

    if reps < 0:
        raise ValueError("Negative `reps` are not allowed.")
    elif reps == 0:
        return A[..., :0]
    elif reps == 1:
        return A

    return concatenate(reps * [A], axis=-1)
