def _ttest_ind_from_stats(mean1, mean2, denom, df):

    d = mean1 - mean2
    t = np.divide(d, denom)
    t, prob = _ttest_finish(df, t)

    return (t, prob)
