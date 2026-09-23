def _distribute_input(
    input_combined,
    input_combined_split_sizes,
    offsets_rearrange_list,
    offsets_rearrange_sizes,
    sharded_dim_size_max,
    world_size,
    input,
    per_sample_weights,
    pg,
):
    """
    In the circumstance of row-wise sharding of weight, we need to distribute
    the sorted lookup IDs of embeddingBag, offsets and per_sample_weights to
    each rank by range. To save the # of communication, we consolidate the
    communication of tensors which shares the same dtype.

    Args:
        input_combined: list of ID to be sent to each rank.
        input_combined_split_sizes: # of bags sent to each rank.
        offsets_rearrange_list: list of starting position of each bag.
        offsets_rearrange_sizes: # of bag offsets sent to each rank.
        sharded_dim_size_max: the max size of the row each rank gets.
        world_size: number of ranks.
        input: tensor to be applied op on.
        per_sample_weights: weights for weighted sum mode.
        pg: process group.

    Returns:
        gathered_input: list of tensors of IDs for lookup and aggregation.
        output_offsets_tensor_list: list of tensors of offsets which specifies the
            boundary of each bag.
        output_split_sizes: list of size of IDs sent from each rank.
        gathered_per_sample_weights: per_sample_weights from each rank.
    """
    # Communicate the length of offset and ID split size to each rank
    # To save the # of communications, we interleave the sizes into one list.
    input_size_list = offsets_rearrange_sizes + input_combined_split_sizes
    input_size_list[::2] = offsets_rearrange_sizes
    input_size_list[1::2] = input_combined_split_sizes
    output_size_list = _communicate_size_to_each_rank(
        input_size_list, world_size * 2, input, pg
    )

    # Perform the modular operation of the 1D tensor to be sent to each rank.
    input_combined = torch.remainder(input_combined, sharded_dim_size_max)
    input_combined_list = list(torch.split(input_combined, input_combined_split_sizes))

    # Covert each offset list to a tensor and combine with the input
    # so we only perform one communication to each rank.
    input_tensor_list = []
    output_tensor_size_list = []
    for idx, input_list in enumerate(offsets_rearrange_list):
        input_tensor_list.append(
            torch.cat(
                (
                    torch.tensor(input_list, dtype=torch.int64, device=input.device),
                    input_combined_list[idx],
                )
            )
        )
        output_tensor_size_list.append(
            output_size_list[2 * idx] + output_size_list[2 * idx + 1]
        )

    output_tensor_list = _communicate_list_to_each_rank(
        input_tensor_list, output_tensor_size_list, input, pg
    )
    output_tensor_list = list(
        torch.split(torch.cat(output_tensor_list), output_size_list)
    )
    output_offsets_tensor_list = output_tensor_list[::2]
    gathered_input = output_tensor_list[1::2]
    output_split_sizes = output_size_list[1::2]

    # If user specifies per_sample_weights we need to communicate
    # them to the corresponding rank.
    gathered_per_sample_weights = None
    if per_sample_weights is not None:
        # Split the 1D tensor per_sample_weights to be sent to each rank.
        per_sample_weights_list = list(
            torch.split(per_sample_weights, input_combined_split_sizes)
        )
        gathered_per_sample_weights = _communicate_list_to_each_rank(
            per_sample_weights_list,
            output_split_sizes,
            input,
            pg,
            tensor_type=per_sample_weights.dtype,
        )

    return (
        gathered_input,
        output_offsets_tensor_list,
        output_split_sizes,
        gathered_per_sample_weights,
    )
