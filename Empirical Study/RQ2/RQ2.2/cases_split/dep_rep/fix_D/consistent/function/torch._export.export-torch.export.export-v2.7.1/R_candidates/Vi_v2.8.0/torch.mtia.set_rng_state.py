def set_rng_state(
    new_state: Tensor, device: Union[int, str, torch.device] = "mtia"
) -> None:
    r"""Sets the random number generator state.

    Args:
        new_state (torch.ByteTensor): The desired state
        device (torch.device or int, optional): The device to set the RNG state.
            Default: ``'mtia'`` (i.e., ``torch.device('mtia')``, the current mtia device).
    """
    warnings.warn(
        "set_rng_state is not implemented in torch.mtia",
        UserWarning,
        stacklevel=2,
    )
