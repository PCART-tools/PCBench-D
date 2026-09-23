def get_lr_injection():
    """
    Gets current value for lr_injection, a multiplier for all base
    learning rates.
    Must set allow_lr_injection=True when building optimizer, as it
    relies on synchronization over CPU.
    """
    return workspace.FetchBlob(_LEARNING_RATE_INJECTION)
