def _packed_sequence_init(data, batch_sizes=None, sorted_indices=None, unsorted_indices=None):
    # type: (Tensor, Optional[Tensor], Optional[Tensor], Optional[Tensor]) -> PackedSequence
    data, batch_sizes, sorted_indices, unsorted_indices = _packed_sequence_init_args(
        data, batch_sizes, sorted_indices, unsorted_indices)
    return PackedSequence(data, batch_sizes, sorted_indices, unsorted_indices)
