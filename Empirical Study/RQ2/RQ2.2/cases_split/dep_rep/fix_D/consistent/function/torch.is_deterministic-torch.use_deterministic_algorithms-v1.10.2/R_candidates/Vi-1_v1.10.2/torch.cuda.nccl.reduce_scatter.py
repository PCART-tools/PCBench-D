def reduce_scatter(inputs: Sequence[torch.Tensor],
                   outputs: Sequence[torch.Tensor],
                   op: int = SUM,
                   streams=None, comms=None) -> None:
    _check_sequence_type(inputs)
    _check_sequence_type(outputs)
    torch._C._nccl_reduce_scatter(inputs, outputs, op, streams, comms)
