def _has_sufficient_memory(device, size):
    if torch.device(device).type == 'cuda':
        if not torch.cuda.is_available():
            return False
        gc.collect()
        torch.cuda.empty_cache()
        return torch.cuda.get_device_properties(device).total_memory - torch.cuda.memory_allocated(device) >= size

    if device == 'xla':
        raise unittest.SkipTest('TODO: Memory availability checks for XLA?')

    if device != 'cpu':
        raise unittest.SkipTest('Unknown device type')

    # CPU
    if not HAS_PSUTIL:
        raise unittest.SkipTest('Need psutil to determine if memory is sufficient')

    # The sanitizers have significant memory overheads
    if TEST_WITH_ASAN or TEST_WITH_TSAN or TEST_WITH_UBSAN:
        effective_size = size * 10
    else:
        effective_size = size

    if psutil.virtual_memory().available < effective_size:
        gc.collect()
    return psutil.virtual_memory().available >= effective_size
