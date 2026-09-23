def check_ppf_ppf(distfn, arg):
    npt.assert_(distfn.ppf(0.5,*arg) < np.inf)
    ppfs = distfn.ppf([0.5,0.9],*arg)
    ppf_s = [distfn._ppf(0.5,*arg), distfn._ppf(0.9,*arg)]
    npt.assert_(np.all(ppfs < np.inf))
    npt.assert_(ppf_s[0] == distfn.ppf(0.5,*arg))
    npt.assert_(ppf_s[1] == distfn.ppf(0.9,*arg))
    npt.assert_(ppf_s[0] == ppfs[0])
    npt.assert_(ppf_s[1] == ppfs[1])
