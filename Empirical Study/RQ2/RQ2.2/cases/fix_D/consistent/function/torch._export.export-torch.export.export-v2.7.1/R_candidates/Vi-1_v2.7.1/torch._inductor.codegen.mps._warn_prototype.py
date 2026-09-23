@functools.cache
def _warn_prototype() -> None:
    import warnings

    warnings.warn(
        "torch.compile for Metal is an early protoype and might not work as expected."
        " For details see https://github.com/pytorch/pytorch/issues/150121",
        stacklevel=2,
    )
