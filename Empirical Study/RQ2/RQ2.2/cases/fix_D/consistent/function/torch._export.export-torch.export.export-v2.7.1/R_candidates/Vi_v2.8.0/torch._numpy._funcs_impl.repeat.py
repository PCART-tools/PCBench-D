def repeat(a: ArrayLike, repeats: ArrayLikeOrScalar, axis=None):
    return torch.repeat_interleave(a, repeats, axis)
