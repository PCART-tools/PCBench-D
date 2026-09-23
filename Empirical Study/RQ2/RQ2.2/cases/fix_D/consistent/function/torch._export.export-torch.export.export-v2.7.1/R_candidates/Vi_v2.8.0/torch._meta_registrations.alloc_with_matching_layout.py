def alloc_with_matching_layout(
    query: Tensor,
    res_shape: tuple[int, ...],
):
    if tuple(query.shape) == res_shape:
        query_t = query.transpose(1, 2)
        res = torch.empty_like(query_t).transpose(1, 2)
    else:
        dim_order = sorted(
            [0, 1, 2, 3], key=lambda idx: query.stride()[idx], reverse=True
        )
        permuted_shape = [res_shape[idx] for idx in dim_order]
        final_permute = [dim_order.index(i) for i in range(len(dim_order))]
        res = torch.empty(
            permuted_shape, dtype=query.dtype, device=query.device
        ).permute(final_permute)

    return res
