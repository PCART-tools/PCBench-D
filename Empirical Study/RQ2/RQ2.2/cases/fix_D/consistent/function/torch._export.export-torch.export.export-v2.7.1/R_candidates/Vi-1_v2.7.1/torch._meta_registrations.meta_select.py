@register_meta(aten.select.int)
def meta_select(self, dim, index):
    from torch.fx.experimental.symbolic_shapes import guard_size_oblivious

    ndim = self.dim()
    torch._check_index(
        ndim != 0,
        lambda: "select() cannot be applied to a 0-dim tensor.",
    )

    dim = dim if dim >= 0 else dim + ndim
    size = self.size(dim)

    torch._check_index(
        not (
            guard_size_oblivious(-index > size) or guard_size_oblivious(index >= size)
        ),
        lambda: f"select(): index {index} out of range for tensor of size "
        f"{self.size()} at dimension {dim}",
    )

    index = index if index >= 0 else index + size

    new_size = list(self.size())
    new_stride = list(self.stride())

    new_storage_offset = self.storage_offset() + index * new_stride[dim]
    del new_size[dim]
    del new_stride[dim]

    return self.as_strided(new_size, new_stride, new_storage_offset)
