def check_shape(_shape, **kwargs):
    """
    For each *key, value* pair in *kwargs*, check that *value* has the shape
    *_shape*, if not, raise an appropriate ValueError.

    *None* in the shape is treated as a "free" size that can have any length.
    e.g. (None, 2) -> (N, 2)

    The values checked must be numpy arrays.

    Examples
    --------
    To check for (N, 2) shaped arrays

    >>> _api.check_shape((None, 2), arg=arg, other_arg=other_arg)
    """
    target_shape = _shape
    for k, v in kwargs.items():
        data_shape = v.shape

        if len(target_shape) != len(data_shape) or any(
                t not in [s, None]
                for t, s in zip(target_shape, data_shape)
        ):
            dim_labels = iter(itertools.chain(
                'MNLIJKLH',
                (f"D{i}" for i in itertools.count())))
            text_shape = ", ".join((str(n)
                                    if n is not None
                                    else next(dim_labels)
                                    for n in target_shape))

            raise ValueError(
                f"{k!r} must be {len(target_shape)}D "
                f"with shape ({text_shape}). "
                f"Your input has shape {v.shape}."
            )
