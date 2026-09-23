def agm(a, b):
    """Arithmetic, Geometric Mean.

    Start with a_0=a and b_0=b and iteratively compute

    a_{n+1} = (a_n+b_n)/2
    b_{n+1} = sqrt(a_n*b_n)

    until a_n=b_n.   The result is agm(a, b)

    agm(a, b)=agm(b, a)
    agm(a, a) = a
    min(a, b) < agm(a, b) < max(a, b)
    """
    s = a + b + 0.0
    return (pi / 4) * s / ellipkm1(4 * a * b / s ** 2)
