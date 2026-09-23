@contextlib.contextmanager
def freeze_rng_state():
    # no_dispatch needed for test_composite_compliance
    # Some OpInfos use freeze_rng_state for rng determinism, but
    # test_composite_compliance overrides dispatch for all torch functions
    # which we need to disable to get and set rng state
    with no_dispatch():
        rng_state = torch.get_rng_state()
        if torch.cuda.is_available():
            cuda_rng_state = torch.cuda.get_rng_state()
    try:
        yield
    finally:
        with no_dispatch():
            if torch.cuda.is_available():
                torch.cuda.set_rng_state(cuda_rng_state)
            torch.set_rng_state(rng_state)
