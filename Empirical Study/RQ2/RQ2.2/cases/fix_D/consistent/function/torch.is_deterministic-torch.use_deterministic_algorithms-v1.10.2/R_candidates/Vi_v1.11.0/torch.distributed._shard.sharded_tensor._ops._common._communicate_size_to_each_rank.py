def _communicate_size_to_each_rank(
    input_size_list, output_size, input, pg, tensor_type=torch.int
):
    """
    In the circumstance of row-wise sharding of weight, we need to first
    communicate the input length to each rank because each rank gets a
    different one.

    Args:
        input_size_list: list of sizes to be sent to each rank.
        output_size: length of the output tensor.
        input: tensor to be applied op on.
        pg: process group.
        tensor_type: dtype of tensor.

    Return: A list of communication results (int).
    """
    input_size_list_tensor = torch.tensor(
        input_size_list, dtype=tensor_type, device=input.device
    )
    output_size_list_tensor = torch.empty(
        output_size, dtype=tensor_type, device=input.device
    )
    dist.all_to_all_single(
        output_size_list_tensor,
        input_size_list_tensor,
        group=pg,
    )
    return output_size_list_tensor.tolist()
