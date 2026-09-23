def reset():
    """Resets all metric counters."""
    torch._C._lazy._reset_metrics()
