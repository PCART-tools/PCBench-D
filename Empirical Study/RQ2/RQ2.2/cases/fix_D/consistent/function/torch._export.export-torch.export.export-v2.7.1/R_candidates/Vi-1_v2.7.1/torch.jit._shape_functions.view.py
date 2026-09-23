def view(self: list[int], sizes: list[int]):
    return infer_size_impl(sizes, numel(self))
