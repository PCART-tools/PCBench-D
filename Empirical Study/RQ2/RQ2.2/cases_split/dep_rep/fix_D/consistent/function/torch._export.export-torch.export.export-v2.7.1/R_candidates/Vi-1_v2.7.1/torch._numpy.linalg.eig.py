@normalizer
@linalg_errors
def eig(a: ArrayLike):
    a = _atleast_float_1(a)
    w, vt = torch.linalg.eig(a)

    if not a.is_complex() and w.is_complex() and (w.imag == 0).all():
        w = w.real
        vt = vt.real
    return w, vt
