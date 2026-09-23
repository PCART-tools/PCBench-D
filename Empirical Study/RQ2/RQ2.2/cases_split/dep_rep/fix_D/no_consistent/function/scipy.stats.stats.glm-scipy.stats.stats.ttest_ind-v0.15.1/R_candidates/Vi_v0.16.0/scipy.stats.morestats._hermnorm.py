def _hermnorm(N):
    # return the negatively normalized hermite polynomials up to order N-1
    #  (inclusive)
    #  using the recursive relationship
    #  p_n+1 = p_n(x)' - x*p_n(x)
    #   and p_0(x) = 1
    plist = [None] * N
    plist[0] = poly1d(1)
    for n in range(1, N):
        plist[n] = plist[n-1].deriv() - poly1d([1, 0]) * plist[n-1]

    return plist
