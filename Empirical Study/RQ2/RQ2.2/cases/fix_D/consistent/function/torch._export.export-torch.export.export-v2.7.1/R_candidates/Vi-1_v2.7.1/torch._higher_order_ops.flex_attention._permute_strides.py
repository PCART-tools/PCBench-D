def _permute_strides(out: torch.Tensor, query_strides: tuple[int, ...]) -> torch.Tensor:
    """
    Create a new tensor with the same data and shape as the input,
    but with strides permuted based on the input tensor's stride order.

    Args:
        out (torch.Tensor): The output tensor of attention.
        query_strides (List[int]): The stride order of the input query tensor

    Returns:
        torch.Tensor: A new tensor with same shape and data as the input,
        but with strides permuted based on the query tensor's stride order.
    """
    from torch._inductor.ir import get_fill_order

    fill_order = get_fill_order(query_strides)
    assert out.storage_offset() == 0, "Only support storage_offset == 0"
    out_strides = _construct_strides(out.shape, fill_order)
    new_out = out.new_empty(out.shape).as_strided(out.shape, out_strides)
    new_out.copy_(out)
    return new_out
