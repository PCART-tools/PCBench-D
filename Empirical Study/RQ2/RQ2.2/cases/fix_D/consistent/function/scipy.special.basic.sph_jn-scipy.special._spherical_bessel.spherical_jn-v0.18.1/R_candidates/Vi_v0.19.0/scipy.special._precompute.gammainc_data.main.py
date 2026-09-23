def main():
    t0 = time()
    # It would be nice to have data for larger values, but either this
    # requires prohibitively large precision (dps > 800) or mpmath has
    # a bug. For example, gammainc(1e20, 1e20, dps=800) returns a
    # value around 0.03, while the true value should be close to 0.5
    # (DLMF 8.12.15).
    print(__doc__)
    pwd = os.path.dirname(__file__)
    r = np.logspace(4, 14, 30)
    ltheta = np.logspace(np.log10(pi/4), np.log10(np.arctan(0.6)), 30)
    utheta = np.logspace(np.log10(pi/4), np.log10(np.arctan(1.4)), 30)
    
    regimes = [(gammainc, ltheta), (gammaincc, utheta)]
    for func, theta in regimes:
        rg, thetag = np.meshgrid(r, theta)
        a, x = rg*np.cos(thetag), rg*np.sin(thetag)
        a, x = a.flatten(), x.flatten()
        dataset = []
        for i, (a0, x0) in enumerate(zip(a, x)):
            if func == gammaincc:
                # Exploit the fast integer path in gammaincc whenever
                # possible so that the computation doesn't take too
                # long
                a0, x0 = np.floor(a0), np.floor(x0)
            dataset.append((a0, x0, func(a0, x0)))
        dataset = np.array(dataset)
        filename = os.path.join(pwd, '..', 'tests', 'data', 'local',
                                '{}.txt'.format(func.__name__))
        np.savetxt(filename, dataset)

    print("{} minutes elapsed".format((time() - t0)/60))
