def from_numpy(a):
    # If not numpy array, piggy back on e.g. tensor guards to check type
    # Re-enable torch function since we disable it on leaf guards
    # we need it to properly construct the tensor if a default device is set
    with torch.overrides._enable_torch_function():
        return torch.as_tensor(a) if isinstance(a, (np.generic, np.ndarray)) else a
