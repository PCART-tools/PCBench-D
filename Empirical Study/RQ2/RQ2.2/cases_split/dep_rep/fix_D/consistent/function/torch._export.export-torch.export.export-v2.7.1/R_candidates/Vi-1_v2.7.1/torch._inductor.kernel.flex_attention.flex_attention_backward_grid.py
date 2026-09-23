def flex_attention_backward_grid(
    batch_size, q_heads, num_queries, d_model, kv_heads, num_key_value, meta
):
    """How is this kernel parallelized?
    Currently this is only parallelizing over batch* kv_heads, but we can, and want to
    parallelize over ceil_div(q_heads//kv_heads * num_key_value, key_value_block_size).
    To do this will either require atomic updates to some grad values or to have a two pass kernel design.
    """
    import triton

    return (
        triton.cdiv(num_queries, meta["BLOCK_M2"]) * (q_heads // kv_heads)
        + triton.cdiv(num_key_value, meta["BLOCK_N1"]),
        1,
        batch_size * kv_heads,
    )
