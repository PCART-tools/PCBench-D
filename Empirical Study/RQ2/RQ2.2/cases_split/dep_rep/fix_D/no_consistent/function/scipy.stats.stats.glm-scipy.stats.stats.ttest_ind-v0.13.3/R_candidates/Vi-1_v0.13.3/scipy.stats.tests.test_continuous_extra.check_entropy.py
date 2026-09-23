def check_entropy(distfn,arg,msg):
    ent = distfn.entropy(*arg)
    #print 'Entropy =', ent
    npt.assert_(not np.isnan(ent), msg + 'test Entropy is nan')
