@torch.library.custom_op("_torch_testing::numpy_mul", mutates_args=())
def numpy_mul(x: Tensor, y: Tensor) -> Tensor:
    return torch.tensor(to_numpy(x) * to_numpy(y), device=x.device)
