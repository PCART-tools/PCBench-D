def all_gather(inputs: Sequence[torch.Tensor], outputs: Sequence[torch.Tensor], streams=None, comms=None) -> None:
    _check_sequence_type(inputs)
    _check_sequence_type(outputs)
    torch._C._nccl_all_gather(inputs, outputs, streams, comms)
