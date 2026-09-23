def _print_benchmark(prefix, nelem, measurements):
    measurements = sorted(measurements)
    _print_cont("%8s:" % prefix)
    for p in [50, 75, 90, 95]:
        v = np.percentile(measurements, p)
        _print_cont("  p%02d:  %1.3fs  %6d/s" % (p, v, nelem / v))
    _print_cont("\n")
