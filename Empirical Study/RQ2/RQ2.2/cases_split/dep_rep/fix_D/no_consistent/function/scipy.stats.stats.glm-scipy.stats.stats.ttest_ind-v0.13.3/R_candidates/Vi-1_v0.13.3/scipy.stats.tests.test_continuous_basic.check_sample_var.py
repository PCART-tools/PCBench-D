def check_sample_var(sv,n, popvar):
    '''
two-sided chisquare test for sample variance equal to hypothesized variance
    '''
    df = n-1
    chi2 = (n-1)*popvar/float(popvar)
    pval = stats.chisqprob(chi2,df)*2
    npt.assert_(pval > 0.01, 'var fail, t,pval = %f, %f, v,sv=%f,%f' % (chi2,pval,popvar,sv))
