def _is_large_block_for_cpu(m, n, k):
    # Thresholds are experimentally determined to reduce Triton CPU compile times
    if m > 128 or n > 128 or k > 128:
        return True
    return m * n > 2**12
