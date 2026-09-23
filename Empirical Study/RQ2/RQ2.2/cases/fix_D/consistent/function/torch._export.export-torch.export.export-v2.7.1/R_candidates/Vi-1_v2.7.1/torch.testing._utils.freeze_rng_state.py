@contextlib.contextmanager
def freeze_rng_state():
    # no_dispatch needed for test_composite_compliance
    # Some OpInfos use freeze_rng_state for rng determinism, but
    # test_composite_compliance overrides dispatch for all torch functions
    # which we need to disable to get and set rng state
    with torch.utils._mode_utils.no_dispatch(), torch._C._DisableFuncTorch():
        rng_state = torch.get_rng_state()
        if torch.cuda.is_available():
            cuda_rng_state = torch.cuda.get_rng_state()
    try:
        yield
    finally:
        # Modes are not happy with torch.cuda.set_rng_state
        # because it clones the state (which could produce a Tensor Subclass)
        # and then grabs the new tensor's data pointer in generator.set_state.
        #
        # In the long run torch.cuda.set_rng_state should probably be
        # an operator.
        #
        # NB: Mode disable is to avoid running cross-ref tests on this seeding
        with torch.utils._mode_utils.no_dispatch(), torch._C._DisableFuncTorch():
            if torch.cuda.is_available():
                torch.cuda.set_rng_state(cuda_rng_state)  # type: ignore[possibly-undefined]
            torch.set_rng_state(rng_state)
