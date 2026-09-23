def _communicate_list_to_each_rank(
    input_tensor_list, output_lists, input, pg, tensor_type=torch.int64
):
    """
    In the circumstance of row-wise sharding of weight, we need to
    communicate a list of input tensors to each rank. Because the
    input could be a list of list, we need to first convert the list
    to a tensor.

    Args:
        input_tensor_list: list of tensors to be sent to each rank.
        output_lists: list of sizes to be obtained from each rank.
        input: tensor to be applied op on.
        pg: process group.
        tensor_type: dtype of tensor.

    Return: A list of communication results (tensors).
    """
    output_tensor_list = []
    for output_list in output_lists:
        output_tensor_list.append(
            torch.empty(output_list, dtype=tensor_type, device=input.device)
        )
    dist.all_to_all(
        output_tensor_list,
        input_tensor_list,
        group=pg,
    )
    return output_tensor_list
