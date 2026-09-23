def _input_split_sort(input, offsets, padding_idx):
    """
    In the circumstance of row-wise sharding of weight, we need to distribute
    the sorted lookup IDs of embeddingBag to each rank by range. The constraint
    here is that we can not directly sort the whole input because we have to
    differentiate between each interval because the result is aggregated.

    If the index in the placement is not equal to the rank number, we need to
    do the rearrangement based on the order given by the Sharding Spec (placement).

    We also calculate the split_size with padding_idx excluded per interval
    so that we can use it as the divisor to calculate the mean correctly.

    Args:
        input: tensor to be applied op on.
        offsets: start index of each interval in the 1D case.
        padding_idx: the embedding vector at padding_idx is
            excluded from the reduction.

    Return:
        input_split_sorted_list: list of ID positions sorted per interval.
        input_split_sorted_indices: sorted indices for per_sample_weights
            rearrangments.
        split_sizes_1d: size of each split for 1D input because it can be
            different in such scenario.
        split_sizes_1d_with_padding: size of each split for 1D input with
            padding_idx excluded. This is for the divisor of `mean` mode.
    """
    input_size = input.size()
    input_split_sorted_list = []
    split_sizes_1d = []
    split_sizes_1d_with_padding = []
    padding_idx = padding_idx if padding_idx is not None else -1

    # For 2D tensor, we just first sort and then append row by row into a list.
    if len(input_size) > 1:
        indice_offset = 0
        sorted_input, input_split_sorted_indices = torch.sort(input)
        for i in range(0, sorted_input.size(0)):
            input_split_sorted_list.append(sorted_input[i])
            input_split_sorted_indices[i] += indice_offset
            indice_offset += input.size(1)
            split_sizes_1d_with_padding.append(
                torch.sum(torch.ne(sorted_input[i], padding_idx)).item()
            )
        input_split_sorted_indices = torch.reshape(input_split_sorted_indices, (-1,))
    # Split 1D input tensor based on the given offsets.
    else:
        input_split_sorted_indices_list = []
        offset_len = len(offsets)
        split_size = offsets[1:offset_len] - offsets[0:-1]
        split_sizes_1d = split_size.tolist()
        if torch.sum(split_size) < input.size(0):
            split_sizes_1d.append(input.size(0) - offsets[-1].item())
        indice_offset = 0
        for idx, split_result in enumerate(torch.split(input, split_sizes_1d)):
            split_result_sorted, indices = torch.sort(split_result)
            input_split_sorted_list.append(split_result_sorted)
            split_sizes_1d_with_padding.append(
                torch.sum(torch.ne(split_result_sorted, padding_idx)).item()
            )
            input_split_sorted_indices_list.append(indices + indice_offset)
            indice_offset += split_sizes_1d[idx]
        input_split_sorted_indices = torch.cat(input_split_sorted_indices_list)

    return (
        input_split_sorted_list,
        input_split_sorted_indices,
        split_sizes_1d,
        split_sizes_1d_with_padding,
    )
