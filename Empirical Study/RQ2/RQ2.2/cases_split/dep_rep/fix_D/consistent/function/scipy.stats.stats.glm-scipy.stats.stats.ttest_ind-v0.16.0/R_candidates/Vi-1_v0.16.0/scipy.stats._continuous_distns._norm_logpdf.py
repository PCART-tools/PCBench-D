def _norm_logpdf(x):
    return -x**2 / 2.0 - _norm_pdf_logC
