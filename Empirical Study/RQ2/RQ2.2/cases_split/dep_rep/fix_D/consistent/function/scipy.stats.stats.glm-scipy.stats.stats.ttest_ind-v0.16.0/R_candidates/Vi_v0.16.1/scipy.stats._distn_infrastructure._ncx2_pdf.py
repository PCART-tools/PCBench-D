def _ncx2_pdf(x, df, nc):
    return np.exp(_ncx2_log_pdf(x, df, nc))
