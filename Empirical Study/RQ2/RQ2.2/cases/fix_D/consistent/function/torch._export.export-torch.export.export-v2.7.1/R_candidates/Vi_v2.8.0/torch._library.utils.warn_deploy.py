def warn_deploy(stacklevel=3):
    warnings.warn(
        "Python torch.library APIs do nothing under torch::deploy (multipy). "
        "Please instead use C++ custom operator registration APIs.",
        RuntimeWarning,
        stacklevel=stacklevel,
    )
