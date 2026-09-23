def norm(x):
    """Compute RMS norm."""
    return np.linalg.norm(x) / x.size ** 0.5
