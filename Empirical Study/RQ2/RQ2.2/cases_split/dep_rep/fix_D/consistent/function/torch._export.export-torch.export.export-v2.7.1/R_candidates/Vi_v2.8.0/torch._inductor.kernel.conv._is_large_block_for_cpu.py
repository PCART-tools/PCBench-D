def _is_large_block_for_cpu(m, n, k):
    # Thresholds are experimentally determined to reduce Triton CPU compile times
    if m > 256 or n > 256 or k > 256:
        return True
    return m * n * k > 2**17
