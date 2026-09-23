def check_distribution(dist, args, alpha):
    D,pval = stats.kstest(dist,'', args=args, N=1000)
    if (pval < alpha):
        D,pval = stats.kstest(dist,'',args=args, N=1000)
        # if (pval < alpha):
        #    D,pval = stats.kstest(dist,'',args=args, N=1000)
        assert_(pval > alpha, msg="D = " + str(D) + "; pval = " + str(pval) +
               "; alpha = " + str(alpha) + "\nargs = " + str(args))
