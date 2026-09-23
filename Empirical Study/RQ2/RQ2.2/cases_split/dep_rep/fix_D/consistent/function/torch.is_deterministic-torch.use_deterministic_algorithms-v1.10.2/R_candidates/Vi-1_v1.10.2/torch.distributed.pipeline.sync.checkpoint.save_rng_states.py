def save_rng_states(device: torch.device, rng_states: Deque[RNGStates],) -> None:
    """:meth:`Checkpoint.forward` captures the current PyTorch's random number
    generator states at CPU and GPU to reuse in :meth:`Recompute.backward`.

    .. seealso:: :ref:`Referential Transparency`

    """
    cpu_rng_state = torch.get_rng_state()

    gpu_rng_state: Optional[Tensor]
    if device.type == "cuda":
        gpu_rng_state = torch.cuda.get_rng_state(device)
    else:
        gpu_rng_state = None

    rng_states.append((cpu_rng_state, gpu_rng_state))
