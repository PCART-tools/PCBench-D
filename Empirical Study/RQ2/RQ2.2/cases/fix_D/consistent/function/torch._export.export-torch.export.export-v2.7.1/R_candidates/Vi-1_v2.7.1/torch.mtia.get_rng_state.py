def get_rng_state(device: Union[int, str, torch.device] = "mtia") -> Tensor:
    r"""Returns the random number generator state as a ByteTensor.

    Args:
        device (torch.device or int, optional): The device to return the RNG state of.
            Default: ``'mtia'`` (i.e., ``torch.device('mtia')``, the current mtia device).
    """
    warnings.warn(
        "get_rng_state is not implemented in torch.mtia",
        UserWarning,
        stacklevel=2,
    )
    return torch.zeros([1], dtype=torch.uint8, device=device)
