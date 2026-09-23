def test_vonmises_pdf_periodic():
    for k in [0.1, 1, 101]:
        for x in [0, 1, numpy.pi, 10, 100]:
            yield check_vonmises_pdf_periodic, k, 0, 1, x
            yield check_vonmises_pdf_periodic, k, 1, 1, x
            yield check_vonmises_pdf_periodic, k, 0, 10, x

            yield check_vonmises_cdf_periodic, k, 0, 1, x
            yield check_vonmises_cdf_periodic, k, 1, 1, x
            yield check_vonmises_cdf_periodic, k, 0, 10, x
