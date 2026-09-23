@lru_cache
def create_block_mask_cached(
    score_mod: _mask_mod_signature,
    B: Optional[int],
    H: Optional[int],
    M: int,
    N: int,
    device: str = "cuda",
) -> BlockMask:
    block_mask = create_block_mask(score_mod, B, H, M, N, device=device)
    return block_mask
