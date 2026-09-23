def validate_tensors_metadata(
    desc,
    expected_tensors: Union[list[torch.Tensor], tuple[torch.Tensor, ...]],
    actual_tensors: Union[list[torch.Tensor], tuple[torch.Tensor, ...]],
):
    if len(expected_tensors) != len(actual_tensors):
        raise PipeliningShapeError(
            f"{desc}: Number of values ({len(actual_tensors)}) does not match expected number ({len(expected_tensors)})"
        )
    for i in range(len(expected_tensors)):
        validate_tensor_metadata(
            f"{desc}: value {i}", expected_tensors[i], actual_tensors[i]
        )
