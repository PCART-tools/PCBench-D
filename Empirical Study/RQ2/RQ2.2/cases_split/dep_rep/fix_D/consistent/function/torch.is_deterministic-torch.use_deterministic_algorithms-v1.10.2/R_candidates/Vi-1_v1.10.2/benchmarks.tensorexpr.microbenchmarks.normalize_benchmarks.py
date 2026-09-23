def normalize_benchmarks(ops):
    return [i + (None,) if len(i) == 3 else i for i in ops]
