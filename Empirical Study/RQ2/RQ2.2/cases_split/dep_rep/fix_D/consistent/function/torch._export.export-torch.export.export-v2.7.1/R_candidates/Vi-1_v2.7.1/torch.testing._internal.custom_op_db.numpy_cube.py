@torch.library.custom_op("_torch_testing::numpy_cube", mutates_args=())
def numpy_cube(x: Tensor) -> tuple[Tensor, Tensor]:
    x_np = to_numpy(x)
    dx = torch.tensor(3 * x_np ** 2, device=x.device)
    return torch.tensor(x_np ** 3, device=x.device), dx
