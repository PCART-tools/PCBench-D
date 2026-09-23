def warn_deprecated():
    warnings.warn(
        "torch._custom_op is deprecated and will be removed in PyTorch 2.6, please "
        "use the equivalent torch.library API instead.", DeprecationWarning)
