def _ncx2_log_pdf(x, df, nc):
    a = asarray(df/2.0)
    fac = -nc/2.0 - x/2.0 + (a-1)*log(x) - a*log(2) - gammaln(a)
    return fac + np.nan_to_num(log(hyp0f1(a, nc * x/4.0)))
