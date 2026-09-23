@_silence_fp_errors
def check_distribution_rvs(dist, args, alpha, rvs):
    # test from scipy.stats.tests
    # this version reuses existing random variables
    D,pval = stats.kstest(rvs, dist, args=args, N=1000)
    if (pval < alpha):
        D,pval = stats.kstest(dist,'',args=args, N=1000)
        npt.assert_(pval > alpha, "D = " + str(D) + "; pval = " + str(pval) +
               "; alpha = " + str(alpha) + "\nargs = " + str(args))
