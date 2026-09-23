@np.deprecate(message="mstats.betai is deprecated in scipy 0.17.0; "
              "use special.betainc instead.")
def betai(a, b, x):
    """
    betai() is deprecated in scipy 0.17.0.

    For details about this function, see `stats.betai`.
    """
    return _betai(a, b, x)
