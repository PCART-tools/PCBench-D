def _handle_row_wise_lookup_distribute(
    input_sorted, input, world_size, weight, rank, padding_idx
):
    """
    In the circumstance of row-wise sharding of weight, we need to distribute
    the sorted lookup IDs of embedding/embeddingBag to each rank.
    If the index in the placement is not equal to the rank number, we need to
    do the rearrangement based on the order given by the Sharding Spec (placement).

    In addition, we do two things for padding_idx. The first thing is to only
    set it if it's within the range of the current rank and the other thing
    is to do the modularization of it by sharded_dim_size_max.

    Args:
        input_sorted: sorted lookup IDs of embedding/embeddingBag.
        input: tensor to be applied op on.
        world_size: number of ranks.
        weight: shareded weight tensor.
        rank: # of cuda process.
        padding_idx: If specified, the entries at padding_idx do
            not contribute to the gradient and reduction.

    Return:
        input_sorted: sorted lookup IDs of embedding/embeddingBag
            Rearrangement performed if it is needed.
        input_split_sizes: size of IDs to be assigned to each rank.
        sharded_dim_size_max: the max size of the row each rank gets.
        input_split_rearrange_indices: indices of row rearrangement.
        rearrange_indices_1d_second_order: reverse indices of row
            rearrangement, which will be used to restore the original
            order.
        padding_idx: Same as input if padding_idx is within the range
            of the given rank; otherwise, None is returned. It is
            also modularized by sharded_dim_size_max.
    """
    # Decide which rank the input goes to by check the sharding range.
    split_size = get_split_size(weight.size(0), world_size)
    rearrange_rows = False
    indices_flatten = None
    input_split_sizes: List[int] = [0] * world_size
    input_split_start_indices: List[int] = [0] * world_size
    start_row_idx_rank = None
    end_row_idx_rank = None
    # When we do the chunk split, we always ensure the first N - 1 chunks get max out
    # and then the Nth chunk gets the rest. So input_split_sizes like [3, 3, 3, 4]
    # are not possible. The expected split size will be [4, 4, 4, 1].
    sharded_dim_size_max = get_chunked_dim_size(weight.size(0), split_size, 0)
    for idx, placement in enumerate(weight._sharding_spec.placements):
        sharded_dim_size = get_chunked_dim_size(weight.size(0), split_size, idx)
        start_row_idx = idx * sharded_dim_size_max
        end_row_idx = start_row_idx + sharded_dim_size
        start_idx = torch.searchsorted(input_sorted, start_row_idx).item()
        end_idx = torch.searchsorted(input_sorted, end_row_idx).item()
        input_split_sizes[placement.rank()] = int(end_idx - start_idx)
        input_split_start_indices[placement.rank()] = int(start_idx)
        if placement.rank() != idx:
            rearrange_rows = True
        # Store the range of the current rank.
        if placement.rank() == rank:
            start_row_idx_rank = start_row_idx
            end_row_idx_rank = end_row_idx

    # Perform the modular if padding_idx is within the range.
    if padding_idx is not None:
        if padding_idx < start_row_idx_rank or padding_idx >= end_row_idx_rank:
            padding_idx = None
        else:
            padding_idx = padding_idx % sharded_dim_size_max

    rearrange_indices_1d_second_order = None
    if rearrange_rows:
        # Need to re-arrange the 1D tensor to be sent via all2all.
        indices: List[List[int]] = [[0]] * world_size
        for placement in weight._sharding_spec.placements:
            split_length = input_split_sizes[placement.rank()]
            offset_idx = input_split_start_indices[placement.rank()]
            indices[placement.rank()] = list(
                range(offset_idx, offset_idx + split_length)
            )
        indices_flatten = list(idx for indice in indices for idx in indice)

        input_sorted = input_sorted.index_select(
            0, torch.tensor(indices_flatten, device=input.device)
        )
        rearrange_indices_1d_second_order = torch.argsort(torch.Tensor(indices_flatten))

    return (
        input_sorted,
        input_split_sizes,
        sharded_dim_size_max,
        torch.tensor(indices_flatten, device=input.device) if rearrange_rows else None,
        rearrange_indices_1d_second_order,
        padding_idx,
    )
