def _transform_integrals(a, b):
    # Transform integrals to a form with finite a < b
    # For b < a, we reverse the limits and will multiply the final result by -1
    # For infinite limit on the right, we use the substitution x = 1/t - 1 + a
    # For infinite limit on the left, we substitute x = -x and treat as above
    # For infinite limits, we substitute x = t / (1-t**2)

    negative = b < a
    a[negative], b[negative] = b[negative], a[negative]

    abinf = np.isinf(a) & np.isinf(b)
    a[abinf], b[abinf] = -1, 1

    ainf = np.isinf(a)
    a[ainf], b[ainf] = -b[ainf], -a[ainf]

    binf = np.isinf(b)
    a0 = a.copy()
    a[binf], b[binf] = 0, 1

    return a, b, a0, negative, abinf, ainf, binf
