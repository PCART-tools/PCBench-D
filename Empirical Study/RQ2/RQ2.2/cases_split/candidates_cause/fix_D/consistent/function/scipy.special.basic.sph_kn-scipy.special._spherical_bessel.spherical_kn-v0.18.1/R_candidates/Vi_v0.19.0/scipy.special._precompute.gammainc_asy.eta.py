def eta(lam):
    """Function from DLMF 8.12.1 shifted to be centered at 0."""
    if lam > 0:
        return mp.sqrt(2*(lam - mp.log(lam + 1)))
    elif lam < 0:
        return -mp.sqrt(2*(lam - mp.log(lam + 1)))
    else:
        return 0
