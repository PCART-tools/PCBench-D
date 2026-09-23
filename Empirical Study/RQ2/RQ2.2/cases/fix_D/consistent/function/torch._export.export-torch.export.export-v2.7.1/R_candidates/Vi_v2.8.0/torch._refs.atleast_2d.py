def atleast_2d(
    arg: Union[TensorLikeType, Sequence[TensorLikeType]], *args: TensorLikeType
) -> Union[TensorLikeType, tuple[TensorLikeType, ...]]:
    """Reference implementation of :func:`torch.atleast_2d`."""
    if not args and isinstance(arg, collections.abc.Sequence):
        args_ = arg
    else:
        assert not isinstance(arg, collections.abc.Sequence)
        args_ = (arg,) + args
    unsqueeze_atleast_1d = partial(_unsqueeze_atleast, atleast_1d, 0)
    res = tuple(a if a.ndim >= 2 else unsqueeze_atleast_1d(a) for a in args_)
    return res if len(res) > 1 else res[0]
