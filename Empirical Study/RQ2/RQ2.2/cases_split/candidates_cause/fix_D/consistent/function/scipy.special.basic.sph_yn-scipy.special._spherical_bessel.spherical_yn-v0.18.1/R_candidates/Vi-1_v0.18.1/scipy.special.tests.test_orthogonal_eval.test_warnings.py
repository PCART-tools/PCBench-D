def test_warnings():
    # ticket 1334
    olderr = np.seterr(all='raise')
    try:
        # these should raise no fp warnings
        orth.eval_legendre(1, 0)
        orth.eval_laguerre(1, 1)
        orth.eval_gegenbauer(1, 1, 0)
    finally:
        np.seterr(**olderr)
