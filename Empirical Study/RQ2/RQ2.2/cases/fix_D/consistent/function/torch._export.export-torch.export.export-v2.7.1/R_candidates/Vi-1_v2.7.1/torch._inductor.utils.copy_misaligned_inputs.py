def copy_misaligned_inputs(
    new_inputs: list[InputType], check_inputs_idxs: Sequence[int]
) -> None:
    for i in check_inputs_idxs:
        _inp = new_inputs[i]
        assert isinstance(_inp, torch.Tensor)
        if _inp.data_ptr() % ALIGNMENT:
            new_inputs[i] = clone_preserve_strides(_inp)
