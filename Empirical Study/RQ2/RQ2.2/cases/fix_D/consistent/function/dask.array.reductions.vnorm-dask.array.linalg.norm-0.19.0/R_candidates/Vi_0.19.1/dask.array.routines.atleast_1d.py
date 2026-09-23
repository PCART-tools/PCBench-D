@wraps(np.atleast_1d)
def atleast_1d(*arys):
    new_arys = []
    for x in arys:
        x = asanyarray(x)
        if x.ndim == 0:
            x = x[None]

        new_arys.append(x)

    if len(new_arys) == 1:
        return new_arys[0]
    else:
        return new_arys
