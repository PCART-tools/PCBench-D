def _unpack_flash_attention_nested_shapes(
    *,
    query,
    key,
    value,
    grad_out=None,
    cum_seq_q,
    cum_seq_k,
    max_q,
    max_k,
) -> Iterator[tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], Optional[tuple[int, ...]]]]:
    """
    Given inputs to a flash_attention_(forward|backward) kernel, this will handle behavior for
    NestedTensor inputs by effectively unbinding the NestedTensor and yielding the shapes for
    each batch element.

    In the case that this isn't a NestedTensor kernel, then it just yields the original shapes.
    """
    if cum_seq_q is not None:
        # This means we should be dealing with a Nested Jagged Tensor query.
        # The inputs will have shape                  (sum(sequence len), heads, dimension)
        # In comparison, non-Nested inputs have shape (batch, heads, sequence len, dimension)
        # To deal with this, we convert to a shape of (batch, heads, max_seq_len, dimension)
        # So the flops calculation in this case is an overestimate of the actual flops.
        assert len(key.shape) == 3
        assert len(value.shape) == 3
        assert grad_out is None or grad_out.shape == query.shape
        _, h_q, d_q = query.shape
        _, h_k, d_k = key.shape
        _, h_v, d_v = value.shape
        assert cum_seq_q is not None
        assert cum_seq_k is not None
        assert cum_seq_q.shape == cum_seq_k.shape
        seq_q_lengths = _offsets_to_lengths(cum_seq_q, max_q)
        seq_k_lengths = _offsets_to_lengths(cum_seq_k, max_k)
        for (seq_q_len, seq_k_len) in zip(seq_q_lengths, seq_k_lengths):
            new_query_shape = (1, h_q, seq_q_len, d_q)
            new_key_shape = (1, h_k, seq_k_len, d_k)
            new_value_shape = (1, h_v, seq_k_len, d_v)
            new_grad_out_shape = new_query_shape if grad_out is not None else None
            yield new_query_shape, new_key_shape, new_value_shape, new_grad_out_shape
        return

    yield query.shape, key.shape, value.shape, grad_out.shape if grad_out is not None else None
