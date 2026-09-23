@register_decomposition(aten.pixel_unshuffle)
@out_wrapper()
def pixel_unshuffle(self: Tensor, downscale_factor: int):
    torch._check(
        self.dim() >= 3,
        lambda: f"pixel_unshuffle expects input to have at least 3 dimensions, but got input with {self.dim} dimension(s)",
    )
    batch = self.shape[:-3]
    C_out = self.shape[-3] * downscale_factor**2
    HW_out = (self.shape[-2] // downscale_factor, self.shape[-1] // downscale_factor)
    n = len(batch)
    B_dims = range(n)
    C_dim, H_dim, r1_dim, W_dim, r2_dim = range(n, n + 5)
    return (
        self.view(
            *batch,
            self.shape[-3],
            HW_out[0],
            downscale_factor,
            HW_out[1],
            downscale_factor,
        )
        .permute(*B_dims, C_dim, r1_dim, r2_dim, H_dim, W_dim)
        .reshape(*batch, C_out, *HW_out)
        .clone(memory_format=utils.suggest_memory_format(self))
    )
