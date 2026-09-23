def create_nested_block_mask(
    mask_mod: _mask_mod_signature,
    B: Optional[int],
    H: Optional[int],
    q_nt: torch.Tensor,
    kv_nt: Optional[torch.Tensor] = None,
    BLOCK_SIZE: Union[int, tuple[int, int]] = _DEFAULT_SPARSE_BLOCK_SIZE,
    _compile=False,
) -> BlockMask:
    r"""This function creates a nested tensor compatible block mask tuple from a mask_mod
    function. The returned BlockMask will be on the device specified by the input nested tensor.

    Args:
        mask_mod (Callable): mask_mod function. This is a callable that defines the
            masking pattern for the attention mechanism. It takes four arguments:
            b (batch size), h (number of heads), q_idx (query index), and kv_idx (key/value index).
            It should return a boolean tensor indicating which attention connections are allowed
            (True) or masked out (False).
        B (int): Batch size.
        H (int): Number of query heads.
        q_nt (torch.Tensor): Jagged layout nested tensor (NJT) that defines the sequence length
            structure for query. The block mask will be constructed to operate on a "stacked
            sequence" of length ``sum(S)`` for sequence length ``S`` from the NJT.
        kv_nt (torch.Tensor): Jagged layout nested tensor (NJT) that defines the sequence length
            structure for key / value, allowing for cross attention. The block mask will be
            constructed to operate on a "stacked sequence" of length ``sum(S)`` for sequence
            length ``S`` from the NJT. If this is None, ``q_nt`` is used to define the structure
            for key / value as well. Default: None
        BLOCK_SIZE (int or tuple[int, int]): Block size for the block mask. If a single int is
            provided it is used for both query and key/value.

    Returns:
        BlockMask:  A BlockMask object that contains the block mask information.

    Example Usage:
        .. code-block:: python

            # shape (B, num_heads, seq_len*, D) where seq_len* varies across the batch
            query = torch.nested.nested_tensor(..., layout=torch.jagged)
            key = torch.nested.nested_tensor(..., layout=torch.jagged)
            value = torch.nested.nested_tensor(..., layout=torch.jagged)

            def causal_mask(b, h, q_idx, kv_idx):
                return q_idx >= kv_idx

            block_mask = create_nested_block_mask(causal_mask, 1, 1, query, _compile=True)
            output = flex_attention(query, key, value, block_mask=block_mask)

        .. code-block:: python

            # shape (B, num_heads, seq_len*, D) where seq_len* varies across the batch
            query = torch.nested.nested_tensor(..., layout=torch.jagged)
            key = torch.nested.nested_tensor(..., layout=torch.jagged)
            value = torch.nested.nested_tensor(..., layout=torch.jagged)

            def causal_mask(b, h, q_idx, kv_idx):
                return q_idx >= kv_idx

            # cross attention case: pass both query and key/value NJTs
            block_mask = create_nested_block_mask(causal_mask, 1, 1, query, key, _compile=True)
            output = flex_attention(query, key, value, block_mask=block_mask)
    """
    # use same structure for kv as for q by default
    if kv_nt is None:
        kv_nt = q_nt
    if q_nt.device != kv_nt.device:
        raise ValueError(
            "create_nested_block_mask(): Expected q_nt and kv_nt to be on the same device"
        )
    return create_block_mask(
        _nested_mod_func_adapter(mask_mod, q_nt, kv_nt, is_score_mod=False),  # type: ignore[arg-type]
        B,
        H,
        q_nt._values.shape[q_nt._ragged_idx - 1],  # type: ignore[attr-defined]
        kv_nt._values.shape[kv_nt._ragged_idx - 1],  # type: ignore[attr-defined]
        device=q_nt.device,  # type: ignore[arg-type]
        # compile is important so we don't materialize a mask_tensor of
        # shape (1, 1, total_seqlen, total_seqlen)
        BLOCK_SIZE=BLOCK_SIZE,
        _compile=_compile,
    )
