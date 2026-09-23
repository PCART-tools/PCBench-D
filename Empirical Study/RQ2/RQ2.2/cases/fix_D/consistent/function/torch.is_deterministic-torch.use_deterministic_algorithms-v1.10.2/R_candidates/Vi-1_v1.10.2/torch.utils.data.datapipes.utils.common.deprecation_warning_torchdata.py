def deprecation_warning_torchdata(name):
    warnings.warn(f"{name} and its functional API are deprecated and will be removed from the package `torch`. "
                  f"Please import those features from the new package TorchData: https://github.com/pytorch/data",
                  DeprecationWarning)
