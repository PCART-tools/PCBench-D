def check_sample_skew_kurt(distfn, arg, sk, ss, msg):
    k,s = distfn.stats(moment='ks',*arg)
    check_sample_meanvar, sk, k, msg + 'sample skew test'
    check_sample_meanvar, ss, s, msg + 'sample kurtosis test'
