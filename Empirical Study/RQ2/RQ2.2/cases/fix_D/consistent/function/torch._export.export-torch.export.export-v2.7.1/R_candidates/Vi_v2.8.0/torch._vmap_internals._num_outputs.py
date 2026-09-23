def _num_outputs(batched_outputs: Union[Tensor, tuple[Tensor, ...]]) -> int:
    if isinstance(batched_outputs, tuple):
        return len(batched_outputs)
    return 1
