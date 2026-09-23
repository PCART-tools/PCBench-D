def _sorted_input_distribute_prepare(
    input_split_sorted_list,
    input_split_sorted_indices,
    world_size,
    input,
    weight,
    per_sample_weights,
    rank,
    padding_idx,
):
    """
    In the circumstance of row-wise sharding of weight, we need to distribute
    the sorted lookup IDs of embeddingBag to each rank by range. After sorting
    per interval, we need to distribute each position to the corresponding
    rank and we need to sync this change to offsets and per_sample_weights.
    Also, we perform rearrangements, if the order in Sharding Spec is not
    same as the rank sequence.

    In addition, in the row-wise sharding, we need to do two things for
    padding_idx. The first thing is only to set it if it's within the range
    of the current rank and the other thing is to do the modularization of
    it by sharded_dim_size_max.

    Args:
        input_split_sorted_list: list of ID positions sorted per interval.
        input_split_sorted_indices: sorted indices for per_sample_weights
            rearrangments.
        input: tensor to be applied op on.
        world_size: number of ranks.
        weight: shareded weight tensor.
        per_sample_weights: weights for weighted sum mode.
        rank: # of cuda process.
        padding_idx: If specified, the entries at padding_idx do
            not contribute to the gradient and reduction.

    Returns:
        input_combined: list of ID to be sent to each rank.
        input_combined_split_sizes: # of bags sent to each rank.
        offsets_rearrange_list: list of starting position of each bag.
        offsets_rearrange_sizes: # of bag offsets sent to each rank.
        per_sample_weights: weights for weighted sum mode.
        sharded_dim_size_max: the max size of the row each rank gets.
        padding_idx: Modularized padding_idx if it is within the range,
            otherwise, None is returned.
    """
    input_sorted_list = []
    input_split_sizes_list = []
    input_split_sizes_rolling_sum = []
    rearrange_indices_list = []
    input_split_rearrange_indices_combined = None
    split_sizes_rolling_sum = 0
    for idx, split_result_sorted in enumerate(input_split_sorted_list):
        split_result_sorted.contiguous()
        (
            input_sorted,
            input_split_sizes,
            sharded_dim_size_max,
            input_split_rearrange_indices,
            _,
            padding_idx_modular,
        ) = _handle_row_wise_lookup_distribute(
            split_result_sorted, input, world_size, weight, rank, padding_idx
        )
        rearrange_indices_list.append(
            input_split_rearrange_indices + split_sizes_rolling_sum
            if input_split_rearrange_indices is not None
            else None
        )
        input_sorted_list.append(input_sorted)
        input_split_sizes_list.append(input_split_sizes)
        input_split_sizes_rolling_sum.append(split_sizes_rolling_sum)
        split_sizes_rolling_sum += sum(input_split_sizes)

    # padding_idx cannot be directly overridden in the for loop because the
    # later iteration will wipe out the modularized padding_idx.
    padding_idx = padding_idx_modular
    if not (any(x is None for x in rearrange_indices_list)):
        input_split_rearrange_indices_combined = torch.cat(rearrange_indices_list)

    # Flatten each interval into a big 1D tensor.
    input_combined = torch.cat(input_sorted_list)

    # Rearrange the 1D tensor to move the IDs of look-up within each
    # interval to the corresponding sharding rank. We also rearrange
    # the offsets to be in sync with IDs.
    input_combined_rearrange_indices = []
    offsets_rearrange_list = []
    offsets_rearrange_sizes = []
    input_combined_split_sizes = []
    # Calculate the indices for rearrangements
    for rank in range(0, world_size):
        offsets_rearrange = []
        offset = 0
        for idx, input_split_sizes in enumerate(input_split_sizes_list):
            offsets_rearrange.append(offset)
            split_length = input_split_sizes[rank]
            offset_idx = input_split_sizes_rolling_sum[idx] + sum(
                [
                    split_size if i < rank else 0
                    for i, split_size in enumerate(input_split_sizes)
                ]
            )
            input_combined_rearrange_indices += list(
                range(offset_idx, offset_idx + split_length)
            )
            offset += split_length
        offsets_rearrange_list.append(offsets_rearrange)
        offsets_rearrange_sizes.append(len(offsets_rearrange))
        input_combined_split_sizes.append(offset)

    # Perform the actual rearrangements of IDs
    input_combined = input_combined.index_select(
        0, torch.tensor(input_combined_rearrange_indices, device=input.device)
    )

    # If per_sample_weights exists, we need to sync the shift which
    # we applied to the position IDs for look-up.
    if per_sample_weights is not None:
        # Rearrange per interval.
        per_sample_weights = torch.reshape(per_sample_weights, (-1,))
        per_sample_weights = per_sample_weights[input_split_sorted_indices]
        if input_split_rearrange_indices_combined is not None:
            per_sample_weights = per_sample_weights[
                input_split_rearrange_indices_combined
            ]
        # Rearrange across different ranks.
        per_sample_weights = per_sample_weights.index_select(
            0,
            torch.tensor(input_combined_rearrange_indices, device=input.device),
        )

    return (
        input_combined,
        input_combined_split_sizes,
        offsets_rearrange_list,
        offsets_rearrange_sizes,
        per_sample_weights,
        sharded_dim_size_max,
        padding_idx,
    )
