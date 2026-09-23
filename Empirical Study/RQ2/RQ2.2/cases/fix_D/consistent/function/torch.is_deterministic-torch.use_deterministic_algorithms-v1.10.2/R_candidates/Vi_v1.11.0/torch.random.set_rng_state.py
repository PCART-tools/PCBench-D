def set_rng_state(new_state: torch.Tensor) -> None:
    r"""Sets the random number generator state.

    .. note: This function only works for CPU. For CUDA, please use
             torch.manual_seed(seed), which works for both CPU and CUDA.

    Args:
        new_state (torch.ByteTensor): The desired state
    """
    default_generator.set_state(new_state)
