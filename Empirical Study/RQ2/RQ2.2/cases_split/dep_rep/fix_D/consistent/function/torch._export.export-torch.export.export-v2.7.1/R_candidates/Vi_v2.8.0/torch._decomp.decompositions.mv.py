@register_decomposition(aten.mv)
@out_wrapper(exact_dtype=True)
@pw_cast_for_opmath
def mv(self, vec):
    torch._check(
        self.dim() == 2 and vec.dim() == 1,
        lambda: f"matrix @ vector expected, got {self.dim()}, {vec.dim()}",
    )
    torch._check(
        self.size(1) == vec.size(0),
        lambda: f"size mismatch, got input ({self.size(0)}x{self.size(1)}), vec ({vec.size(0)})",
    )
    return (self * vec).sum(dim=1)
