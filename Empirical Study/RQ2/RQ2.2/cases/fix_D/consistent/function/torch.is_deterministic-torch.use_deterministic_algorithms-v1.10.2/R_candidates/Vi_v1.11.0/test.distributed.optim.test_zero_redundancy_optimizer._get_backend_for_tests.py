def _get_backend_for_tests():
    return (
        dist.Backend.NCCL if not IS_WINDOWS and torch.cuda.is_available()
        # Windows only has GLOO, but GLOO GPU works. And use GLOO CPU when
        # no GPUs are available.
        else dist.Backend.GLOO
    )
