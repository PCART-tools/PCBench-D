@np.deprecate_with_doc("`oneway` was deprecated in scipy 0.13.0 and will be "
                       "removed in 0.14.0.  Use `f_oneway` instead.")
def oneway(*args,**kwds):
    """Test for equal means in two or more samples from the
    normal distribution.

    If the keyword parameter <equal_var> is true then the variances
    are assumed to be equal, otherwise they are not assumed to
    be equal (default).

    Return test statistic and the p-value giving the probability
    of error if the null hypothesis (equal means) is rejected at this value.
    """
    k = len(args)
    if k < 2:
        raise ValueError("Must enter at least two input sample vectors.")
    if 'equal_var' in kwds:
        if kwds['equal_var']:
            evar = 1
        else:
            evar = 0
    else:
        evar = 0

    Ni = array([len(args[i]) for i in range(k)])
    Mi = array([np.mean(args[i], axis=0) for i in range(k)])
    Vi = array([np.var(args[i]) for i in range(k)])
    Wi = Ni / Vi
    swi = sum(Wi,axis=0)
    N = sum(Ni,axis=0)
    my = sum(Mi*Ni,axis=0)*1.0/N
    tmp = sum((1-Wi/swi)**2 / (Ni-1.0),axis=0)/(k*k-1.0)
    if evar:
        F = ((sum(Ni*(Mi-my)**2,axis=0) / (k-1.0)) / (sum((Ni-1.0)*Vi,axis=0) / (N-k)))
        pval = distributions.f.sf(F,k-1,N-k)  # 1-cdf
    else:
        m = sum(Wi*Mi,axis=0)*1.0/swi
        F = sum(Wi*(Mi-m)**2,axis=0) / ((k-1.0)*(1+2*(k-2)*tmp))
        pval = distributions.f.sf(F,k-1.0,1.0/(3*tmp))

    return F, pval
