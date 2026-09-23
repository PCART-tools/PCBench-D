@wraps(np.vdot)
def vdot(a, b):
    return dot(a.conj().ravel(), b.ravel())
