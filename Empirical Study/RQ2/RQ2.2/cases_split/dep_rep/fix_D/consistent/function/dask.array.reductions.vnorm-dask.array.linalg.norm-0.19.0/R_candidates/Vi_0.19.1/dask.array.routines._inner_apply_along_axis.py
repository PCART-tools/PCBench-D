def _inner_apply_along_axis(arr,
                            func1d,
                            func1d_axis,
                            func1d_args,
                            func1d_kwargs):
    return np.apply_along_axis(
        func1d, func1d_axis, arr, *func1d_args, **func1d_kwargs
    )
