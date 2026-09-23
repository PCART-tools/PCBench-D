def main():
    # It would be nice to have data for larger values, but either this
    # requires prohibitively large precision (dps > 800) or mpmath has
    # a bug. For example, gammainc(1e20, 1e20, dps=800) returns a
    # value around 0.03, while the true value should be close to 0.5
    # (DLMF 8.12.15).
    rmax = 14
    t0 = time()
    print(__doc__)
    # Region where 0.6 <= x/a <= 1. The transition to the asymptotic
    # series begins at x/a = 0.7.
    r = np.logspace(4, rmax, 30)
    theta = np.logspace(np.log10(pi/4), np.log10(np.arctan(0.6)), 30)
    r, theta = np.meshgrid(r, theta)
    a, x = r*np.cos(theta), r*np.sin(theta)
    a, x = a.flatten(), x.flatten()
    dataset = []
    for i, (a0, x0) in enumerate(zip(a, x)):
        dataset.append((a0, x0, gammainc(a0, x0)))
    dataset = np.array(dataset)

    fn = os.path.join(os.path.dirname(__file__), '..', 'tests',
                      'data', 'local', 'gammainc.txt')
    np.savetxt(fn, dataset)
    print("{} minutes elapsed".format((time() - t0)/60))
