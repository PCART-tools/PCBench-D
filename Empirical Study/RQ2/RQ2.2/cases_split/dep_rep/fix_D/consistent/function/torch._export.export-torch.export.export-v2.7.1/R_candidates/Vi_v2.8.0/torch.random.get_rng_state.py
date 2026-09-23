def get_rng_state() -> torch.Tensor:
    r"""Returns the random number generator state as a `torch.ByteTensor`.

    .. note:: The returned state is for the default generator on CPU only.

    See also: :func:`torch.random.fork_rng`.
    """
    return default_generator.get_state()
