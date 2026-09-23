def _nested_mod_func_adapter(
    orig_mod_func: Union[_score_mod_signature, _mask_mod_signature],
    q_nt: torch.Tensor,
    kv_nt: torch.Tensor,
    is_score_mod: bool,
) -> Union[_score_mod_signature, _mask_mod_signature]:
    r"""Adapter to convert a score_mod / mask_mod to be NJT-compatible. The given mod func
    should be written as if operating over a single sequence at a item. This adapter will
    handle conversion from indices operating over a "stacked sequence" of length ``sum(S)``
    for sequence length ``S`` in the NJT to "sequence relative" indices in range ``[0, S)``.

    Args:
        orig_mod_func (Callable): Function to modify attention scores. It takes four or five
            arguments, depending on whether a mask_mod or score_mod func is passed.
        q_nt (torch.Tensor): Jagged layout nested tensor (NJT) that defines the sequence length
            structure for query.
        kv_nt (torch.Tensor): Jagged layout nested tensor (NJT) that defines the sequence length
            structure for key / value.
        is_score_mod (bool): Indicates whether the mod function is a score_mod.

    Returns:
        nt_score_mod: An NJT-compatible version of orig_score_mod
    """

    # Used to convert indices within the "stacked" sequence (range [0, sum(*)))
    # to "sequence local" indices (range [0, S) for each S).
    def _build_seq_idx(offsets, total_length):
        range_tensor = torch.arange(
            total_length, device=offsets.device, dtype=torch.int32
        )

        # Use searchsorted to find the index for each position
        # NB: This assumes offsets[0] to offsets[-1] spans the packed dim of values.
        # If we ever loosen this restriction, this logic will need to be updated.
        seq_idx = torch.searchsorted(offsets, range_tensor, right=True) - 1
        return seq_idx

    q_offsets = q_nt._offsets  # type: ignore[attr-defined]
    kv_offsets = kv_nt._offsets  # type: ignore[attr-defined]
    q_seq_idx = _build_seq_idx(q_offsets, q_nt._values.shape[q_nt._ragged_idx - 1])  # type: ignore[attr-defined]
    if q_nt is kv_nt:
        kv_seq_idx = q_seq_idx
    else:
        # cross attention case
        kv_seq_idx = _build_seq_idx(
            kv_offsets,
            kv_nt._values.shape[kv_nt._ragged_idx - 1],  # type: ignore[attr-defined]
        )

    # Converts q_idx / kv_idx from [0, total_length) -> [0, S), where S refers
    # to the sequence length for each sequence in the NJT, for use in given
    # score_mod. This allows the user to write a score_mod as if it were
    # operating on a single sequence and the "stacked sequence" is split
    # automatically into individual sequences for them.
    if is_score_mod:

        def nt_score_mod(score, b, h, q_idx, kv_idx):
            b_nested = q_seq_idx[q_idx]
            q_nested = q_idx - q_offsets[q_seq_idx[q_idx]]
            kv_nested = kv_idx - kv_offsets[kv_seq_idx[kv_idx]]
            is_same_sequence = q_seq_idx[q_idx] == kv_seq_idx[kv_idx]
            return torch.where(
                is_same_sequence,
                orig_mod_func(score, b_nested, h, q_nested, kv_nested),  # type: ignore[call-arg]
                # don't allow inter-sequence attention
                float("-inf"),
            )

        return nt_score_mod
    else:

        def nt_mask_mod(b, h, q_idx, kv_idx):
            b_nested = q_seq_idx[q_idx]
            q_nested = q_idx - q_offsets[q_seq_idx[q_idx]]
            kv_nested = kv_idx - kv_offsets[kv_seq_idx[kv_idx]]
            # don't allow inter-sequence attention
            is_same_sequence = q_seq_idx[q_idx] == kv_seq_idx[kv_idx]
            return orig_mod_func(b_nested, h, q_nested, kv_nested) & is_same_sequence  # type: ignore[call-arg]

        return nt_mask_mod
