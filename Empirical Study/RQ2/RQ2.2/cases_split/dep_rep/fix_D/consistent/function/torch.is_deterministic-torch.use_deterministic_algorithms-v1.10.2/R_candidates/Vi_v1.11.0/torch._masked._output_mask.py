def _output_mask(op, input: Tensor, *args, **kwargs) -> Tensor:
    """Return output mask of masked operation applied to given arguments.
    """
    if callable(op):
        is_reduction = op.__name__ in {'sum', 'prod', 'amax', 'amin', 'mean', 'norm', 'var'}
        is_normalization = op.__name__ in {'softmax', 'log_softmax', 'softmin', 'normalize'}
        if is_reduction:
            if op.__name__ == 'norm':
                if args:
                    args = args[1:]  # lstrip ord argument
            dim = args[0] if args else kwargs.get('dim')
            outmask = _input_mask(input, *args, **kwargs)
            keepdim = kwargs.get('keepdim', False)
            dim_ = _canonical_dim(dim, input.ndim)
            # Workaround https://github.com/pytorch/pytorch/issues/56586
            for d in reversed(dim_):
                outmask = outmask.any(dim=d, keepdim=bool(keepdim))
            return outmask
        elif is_normalization:
            return _input_mask(input, *args, **kwargs)
        else:
            raise ValueError(f'_output_mask expected masked operation (got callable {op.__module__}.{op.__name__})')
    else:
        raise ValueError(f'_output_mask expected masked operation (got {type(op).__name__} object)')
