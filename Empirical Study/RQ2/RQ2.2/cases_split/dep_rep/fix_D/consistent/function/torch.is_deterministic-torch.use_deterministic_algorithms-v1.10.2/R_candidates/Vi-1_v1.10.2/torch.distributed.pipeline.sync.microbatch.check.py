def check(first_device, *inputs) -> None:
    """
    Checks whether the input contains at least one tensor and each tensor is
    on the same device as the first partition.

    Raises:
        ValueError: input does not contain at least one tensor

    """

    if not any(torch.is_tensor(input) for input in inputs):
        raise TypeError(f'inputs do not have any tensors: {inputs}')
    if any(torch.is_tensor(input) and input.device != first_device for input in inputs):
        raise ValueError('All inputs should be on the same device as the first partition')
