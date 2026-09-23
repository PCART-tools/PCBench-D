def _print_benchmark(prefix, nelem, measurements):
    measurements = sorted(measurements)
    _print_cont(f"{prefix:8s}:")
    for p in [50, 75, 90, 95]:
        v = np.percentile(measurements, p)
        _print_cont(f"  p{p:02d}:  {v:1.3f}s  {nelem / v:6d}/s")
    _print_cont("\n")
