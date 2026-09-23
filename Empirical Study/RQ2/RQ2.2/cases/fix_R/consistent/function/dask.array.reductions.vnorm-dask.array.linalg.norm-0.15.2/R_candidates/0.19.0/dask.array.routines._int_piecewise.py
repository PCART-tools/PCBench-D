def _int_piecewise(x, *condlist, **kwargs):
    return np.piecewise(
        x, list(condlist), kwargs["funclist"],
        *kwargs["func_args"], **kwargs["func_kw"]
    )
