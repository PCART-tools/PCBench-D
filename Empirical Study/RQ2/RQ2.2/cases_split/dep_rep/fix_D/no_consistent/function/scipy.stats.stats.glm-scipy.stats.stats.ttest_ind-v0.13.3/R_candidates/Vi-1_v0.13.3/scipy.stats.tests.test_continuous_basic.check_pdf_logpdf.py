@_silence_fp_errors
def check_pdf_logpdf(distfn, args, msg):
    # compares pdf at several points with the log of the pdf
    points = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    vals = distfn.ppf(points, *args)
    pdf = distfn.pdf(vals, *args)
    logpdf = distfn.logpdf(vals, *args)
    pdf = pdf[pdf != 0]
    logpdf = logpdf[np.isfinite(logpdf)]
    npt.assert_almost_equal(np.log(pdf), logpdf, decimal=7, err_msg=msg + " - logpdf-log(pdf) relationship")
