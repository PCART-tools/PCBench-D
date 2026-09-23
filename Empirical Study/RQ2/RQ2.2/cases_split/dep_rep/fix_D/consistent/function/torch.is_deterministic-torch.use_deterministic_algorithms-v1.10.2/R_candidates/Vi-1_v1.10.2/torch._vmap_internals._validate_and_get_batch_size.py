def _validate_and_get_batch_size(
        flat_in_dims: List[Optional[int]],
        flat_args: List) -> int:
    batch_sizes = [arg.size(in_dim) for in_dim, arg in zip(flat_in_dims, flat_args)
                   if in_dim is not None]
    if batch_sizes and any([size != batch_sizes[0] for size in batch_sizes]):
        raise ValueError(
            f'vmap: Expected all tensors to have the same size in the mapped '
            f'dimension, got sizes {batch_sizes} for the mapped dimension')
    return batch_sizes[0]
