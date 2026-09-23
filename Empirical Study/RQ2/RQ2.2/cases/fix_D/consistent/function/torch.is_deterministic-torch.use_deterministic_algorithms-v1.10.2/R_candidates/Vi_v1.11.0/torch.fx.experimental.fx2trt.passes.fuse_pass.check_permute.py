def check_permute(node: torch.fx.Node):
    ranks = len(node.meta["tensor_meta"].shape)
    permutation = list(i % ranks for i in node.kwargs["permutation"])  # type: ignore[union-attr]
    allowed_permutation = list(i for i in range(ranks))
    allowed_permutation[-1] = ranks - 2
    allowed_permutation[-2] = ranks - 1
    return permutation == allowed_permutation
