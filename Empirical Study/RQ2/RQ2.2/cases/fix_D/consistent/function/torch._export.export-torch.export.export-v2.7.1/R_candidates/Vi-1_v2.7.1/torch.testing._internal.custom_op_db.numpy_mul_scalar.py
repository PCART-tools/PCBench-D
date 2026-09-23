@torch.library.custom_op("_torch_testing::numpy_mul_scalar", mutates_args=())
def numpy_mul_scalar(x: Tensor, *, scalar: float) -> Tensor:
    return torch.tensor(to_numpy(x) * scalar, device=x.device)
