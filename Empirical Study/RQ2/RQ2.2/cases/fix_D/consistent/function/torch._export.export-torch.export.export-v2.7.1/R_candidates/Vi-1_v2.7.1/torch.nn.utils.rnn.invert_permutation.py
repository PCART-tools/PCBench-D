def invert_permutation(permutation: Optional[Tensor]) -> Optional[Tensor]:
    if permutation is None:
        return None
    output = torch.empty_like(permutation, memory_format=torch.legacy_contiguous_format)
    output.scatter_(
        0, permutation, torch.arange(0, permutation.numel(), device=permutation.device)
    )
    return output
