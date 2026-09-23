def set_lr_injection(lr_injection_value):
    """
    Sets lr_injection, a multiplier for all base learning rates.
    Must set allow_lr_injection=True when building optimizer, as it
    relies on synchronization over CPU.
    """
    workspace.FeedBlob(
        _LEARNING_RATE_INJECTION,
        np.array([float(lr_injection_value)], dtype=np.float32),
    )
