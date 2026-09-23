def _is_large_block_for_cpu(m, n, k):
    # Thresholds are experimentally determined to reduce Triton CPU compile times
    return m * n > 2**13
