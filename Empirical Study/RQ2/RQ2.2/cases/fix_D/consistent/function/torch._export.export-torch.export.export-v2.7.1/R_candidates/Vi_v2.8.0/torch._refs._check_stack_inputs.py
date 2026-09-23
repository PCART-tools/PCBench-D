def _check_stack_inputs(tensors: TensorSequenceType) -> None:
    entry_shape = tensors[0].shape
    for i in range(1, len(tensors)):
        assert tensors[i].shape == entry_shape, (
            f"stack expects each tensor to be equal size, but got {entry_shape} at entry 0 "
            f"and {tensors[i].shape} at entry {i}"
        )
