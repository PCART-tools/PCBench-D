@doc_wraps(scipy.stats.chisquare)
def chisquare(f_obs, f_exp=None, ddof=0, axis=0):
    return power_divergence(f_obs, f_exp=f_exp, ddof=ddof, axis=axis,
                            lambda_="pearson")
