@register_decomposition(aten.split_with_sizes)
def split_with_sizes(
    self: Tensor, split_sizes: list[int], dim: int = 0
) -> list[Tensor]:
    # NB: Perform the check_is_size tests first so that the
    # sum test does not try to do a replacement
    for i in range(len(split_sizes)):
        torch._check_is_size(
            split_sizes[i],
            lambda: "split_with_sizes expects split_sizes have only non-negative entries",
        )
    torch._check_with(
        ValueError,
        builtins.sum(split_sizes) == self.shape[dim],
        lambda: f"Split sizes add up to {builtins.sum(split_sizes)} but got the tensor's size of {self.shape[dim]}",
    )

    splits = []
    offset = self.storage_offset()

    for split_size in split_sizes:
        new_shape = list(self.shape)
        new_shape[dim] = split_size
        # We reimplement narrow here to avoid a lot of checks in the
        # decomposition of narrow which calls slice_in_dim and slice
        splits.append(self.as_strided(new_shape, self.stride(), offset))
        offset = offset + self.stride()[dim] * split_size
    return splits
