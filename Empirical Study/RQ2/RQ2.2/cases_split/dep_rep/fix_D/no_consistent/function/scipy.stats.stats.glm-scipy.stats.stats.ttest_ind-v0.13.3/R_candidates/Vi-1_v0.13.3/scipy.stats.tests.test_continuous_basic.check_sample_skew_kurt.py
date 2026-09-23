def check_sample_skew_kurt(distfn, arg, ss, sk, msg):
    skew,kurt = distfn.stats(moments='sk',*arg)
##    skew = distfn.stats(moment='s',*arg)[()]
##    kurt = distfn.stats(moment='k',*arg)[()]
    check_sample_meanvar(sk, kurt, msg + 'sample kurtosis test')
    check_sample_meanvar(ss, skew, msg + 'sample skew test')
